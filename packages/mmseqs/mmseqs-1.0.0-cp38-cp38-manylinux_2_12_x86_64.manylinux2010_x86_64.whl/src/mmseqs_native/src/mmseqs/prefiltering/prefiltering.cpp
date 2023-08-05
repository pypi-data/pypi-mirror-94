#include <mmseqs/prefiltering/prefiltering.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/prefiltering/extendedSubstitutionMatrix.h>
#include <mmseqs/commons/nucleotideMatrix.h>
#include <mmseqs/prefiltering/reducedMatrix.h>
#include <mmseqs/commons/substitutionMatrixProfileStates.h>
#include <mmseqs/output.h>

#include <sys/mman.h>
#include <mmseqs/commons/byteParser.h>
#include <mmseqs/commons/fastSort.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/prefiltering/indexBuilder.h>
#include <mmseqs/commons/memoryMapped.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/patternCompiler.h>
#include <mmseqs/commons/timer.h>

#ifdef OPENMP
#include <omp.h>
#endif

Prefiltering::Prefiltering(mmseqs_output *out, const std::string &queryDB,
                           const std::string &queryDBIndex,
                           const std::string &targetDB,
                           const std::string &targetDBIndex, int querySeqType,
                           int targetSeqType, const Parameters &par)
    : queryDB(queryDB),
      queryDBIndex(queryDBIndex),
      targetDB(targetDB),
      targetDBIndex(targetDBIndex),
      splits(par.split),
      kmerSize(par.kmerSize),
      spacedKmerPattern(par.spacedKmerPattern),
      localTmp(par.localTmp),
      spacedKmer(par.spacedKmer != 0),
      maskMode(par.maskMode),
      maskLowerCaseMode(par.maskLowerCaseMode),
      splitMode(par.splitMode),
      scoringMatrixFile(par.scoringMatrixFile),
      seedScoringMatrixFile(par.seedScoringMatrixFile),
      targetSeqType(targetSeqType),
      maxResListLen(par.maxResListLen),
      kmerScore(par.kmerScore),
      sensitivity(par.sensitivity),
      maxSeqLen(par.maxSeqLen),
      querySeqType(querySeqType),
      diagonalScoring(par.diagonalScoring),
      minDiagScoreThr(static_cast<unsigned int>(par.minDiagScoreThr)),
      aaBiasCorrection(par.compBiasCorrection != 0),
      covThr(par.covThr),
      covMode(par.covMode),
      includeIdentical(par.includeIdentity),
      preloadMode(par.preloadMode),
      threads(static_cast<unsigned int>(par.threads)),
      compressed(par.compressed) {
  sameQTDB = isSameQTDB(out);

  // init the substitution matrices
  switch (querySeqType & 0x7FFFFFFF) {
    case Parameters::DBTYPE_NUCLEOTIDES:
      kmerSubMat = getSubstitutionMatrix(out, scoringMatrixFile, par.alphabetSize,
                                         1.0, false, true);
      ungappedSubMat = kmerSubMat;
      alphabetSize = kmerSubMat->alphabetSize;
      break;
    case Parameters::DBTYPE_AMINO_ACIDS:
      kmerSubMat = getSubstitutionMatrix(out, seedScoringMatrixFile,
                                         par.alphabetSize, 8.0, false, false);
      ungappedSubMat = getSubstitutionMatrix(
          out, scoringMatrixFile, par.alphabetSize, 2.0, false, false);
      alphabetSize = kmerSubMat->alphabetSize;
      break;
    case Parameters::DBTYPE_HMM_PROFILE:
      // needed for Background distributions
      kmerSubMat = getSubstitutionMatrix(out, scoringMatrixFile, par.alphabetSize,
                                         8.0, false, false);
      ungappedSubMat = getSubstitutionMatrix(
          out, scoringMatrixFile, par.alphabetSize, 2.0, false, false);
      alphabetSize = kmerSubMat->alphabetSize;
      break;
    case Parameters::DBTYPE_PROFILE_STATE_PROFILE:
      kmerSubMat = getSubstitutionMatrix(out, scoringMatrixFile, par.alphabetSize,
                                         8.0, true, false);
      ungappedSubMat = getSubstitutionMatrix(
          out, scoringMatrixFile, par.alphabetSize, 2.0, false, false);
      alphabetSize = kmerSubMat->alphabetSize;
      break;
    default:
      out->failure("Query sequence type not implemented");
  }

  if (Parameters::isEqualDbtype(FileUtil::parseDbType(out, targetDB.c_str()),
                                Parameters::DBTYPE_INDEX_DB)) {
    if (preloadMode == Parameters::PRELOAD_MODE_AUTO) {
      if (sensitivity > 6.0) {
        preloadMode = Parameters::PRELOAD_MODE_FREAD;
      } else {
        preloadMode = Parameters::PRELOAD_MODE_MMAP_TOUCH;
      }
    }

    tidxdbr = new DBReader<unsigned int>(
        out,
        targetDB.c_str(), targetDBIndex.c_str(), threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    tidxdbr->open(DBReader<unsigned int>::NOSORT);

    templateDBIsIndex = PrefilteringIndexReader::checkIfIndexFile(tidxdbr);
    if (templateDBIsIndex == true) {
      tdbr = PrefilteringIndexReader::openNewReader(
          out,
          tidxdbr, PrefilteringIndexReader::DBR1DATA,
          PrefilteringIndexReader::DBR1INDEX, false, threads, false, false);
      PrefilteringIndexReader::printSummary(out, tidxdbr);
      PrefilteringIndexData data =
          PrefilteringIndexReader::getMetadata(tidxdbr);
      for (size_t i = 0; i < par.prefilter.size(); i++) {
        if (par.prefilter[i]->wasSet == false) {
          continue;
        }
        if (par.prefilter[i]->uniqid == par.PARAM_K.uniqid) {
          if (kmerSize != 0 && data.kmerSize != kmerSize) {
            out->warn("Index was created with -k {} but the prefilter was called with -k {}", data.kmerSize, kmerSize);
          }
        }
        if (par.prefilter[i]->uniqid == par.PARAM_ALPH_SIZE.uniqid) {
          if (data.alphabetSize != alphabetSize) {
            out->warn("Index was created with --alph-size {} but the prefilter was called with --alph-size {}", data.alphabetSize, alphabetSize);
          }
        }
        if (par.prefilter[i]->uniqid == par.PARAM_SPACED_KMER_MODE.uniqid) {
          if (data.spacedKmer != spacedKmer) {
            out->warn("Index was created with --spaced-kmer-mode {} but the prefilter was called with --spaced-kmer-mode {}", data.spacedKmer, spacedKmer);
          }
        }
        if (par.prefilter[i]->uniqid == par.PARAM_NO_COMP_BIAS_CORR.uniqid) {
          if (data.compBiasCorr != aaBiasCorrection &&
              Parameters::isEqualDbtype(targetSeqType,
                                        Parameters::DBTYPE_HMM_PROFILE)) {
            out->warn("Index was created with --comp-bias-corr {} but the prefilter was called with --comp-bias-corr {}", data.compBiasCorr, aaBiasCorrection);
          }
        }
        if (par.prefilter[i]->uniqid == par.PARAM_SPLIT.uniqid) {
          if (splitMode == Parameters::TARGET_DB_SPLIT &&
              data.splits != splits) {
            out->warn("Index was created with --splits {} but the prefilter was called with --splits {}", data.splits, splits);
          }
        }
      }

      kmerSize = data.kmerSize;
      alphabetSize = data.alphabetSize;
      targetSeqType = data.seqType;
      spacedKmer = data.spacedKmer == 1 ? true : false;
      // the query database could have longer sequences than the target
      // database, do not cut them short
      maxSeqLen = std::max(maxSeqLen, (size_t)data.maxSeqLength);
      aaBiasCorrection = data.compBiasCorr;

      if (Parameters::isEqualDbtype(querySeqType,
                                    Parameters::DBTYPE_HMM_PROFILE) &&
          Parameters::isEqualDbtype(targetSeqType,
                                    Parameters::DBTYPE_HMM_PROFILE)) {
        out->failure("Query-profiles cannot be searched against a target-profile database");
      }

      splits = data.splits;
      if (data.splits > 1) {
        splitMode = Parameters::TARGET_DB_SPLIT;
      }
      spacedKmer = data.spacedKmer != 0;
      spacedKmerPattern = PrefilteringIndexReader::getSpacedPattern(tidxdbr);
      seedScoringMatrixFile = MultiParam<char *>(
          PrefilteringIndexReader::getSubstitutionMatrix(tidxdbr));
    } else {
      out->failure("Outdated index version. Please recompute it with 'createindex'");
    }
  } else {
    tdbr = new DBReader<unsigned int>(
        out,
        targetDB.c_str(), targetDBIndex.c_str(), threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    tdbr->open(DBReader<unsigned int>::LINEAR_ACCCESS);
    templateDBIsIndex = false;
  }

  // restrict amount of allocated memory if all results are requested
  // INT_MAX would allocate 72GB RAM per thread for no reason
  maxResListLen = std::min(tdbr->getSize(), maxResListLen);

  // investigate if it makes sense to mask the profile consensus sequence
  if (Parameters::isEqualDbtype(targetSeqType,
                                Parameters::DBTYPE_HMM_PROFILE) ||
      Parameters::isEqualDbtype(targetSeqType,
                                Parameters::DBTYPE_PROFILE_STATE_SEQ)) {
    maskMode = 0;
  }

  takeOnlyBestKmer =
      (par.exactKmerMatching == 1) ||
      (Parameters::isEqualDbtype(targetSeqType,
                                 Parameters::DBTYPE_HMM_PROFILE) &&
       Parameters::isEqualDbtype(querySeqType,
                                 Parameters::DBTYPE_AMINO_ACIDS)) ||
      (Parameters::isEqualDbtype(targetSeqType,
                                 Parameters::DBTYPE_NUCLEOTIDES) &&
       Parameters::isEqualDbtype(querySeqType, Parameters::DBTYPE_NUCLEOTIDES));

  // memoryLimit in bytes
  size_t memoryLimit = Util::computeMemory(out, par.splitMemoryLimit);

  if (templateDBIsIndex == false && sameQTDB == true) {
    qdbr = tdbr;
  } else {
    qdbr = new DBReader<unsigned int>(
        out,
        queryDB.c_str(), queryDBIndex.c_str(), threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    qdbr->open(DBReader<unsigned int>::LINEAR_ACCCESS);
  }

  out->info("Query database size: {}, type: {}", qdbr->getSize(), Parameters::getDbTypeName(querySeqType));
  setupSplit(out, *tdbr, alphabetSize - 1, querySeqType, threads, templateDBIsIndex,
             memoryLimit, qdbr->getSize(), maxResListLen, kmerSize, splits,
             splitMode);

  if (Parameters::isEqualDbtype(targetSeqType,
                                Parameters::DBTYPE_NUCLEOTIDES) == false) {
    const bool isProfileSearch =
        Parameters::isEqualDbtype(querySeqType,
                                  Parameters::DBTYPE_HMM_PROFILE) ||
        Parameters::isEqualDbtype(targetSeqType,
                                  Parameters::DBTYPE_HMM_PROFILE);
    kmerThr =
        getKmerThreshold(out, sensitivity, isProfileSearch, kmerScore, kmerSize);
  } else {
    kmerThr = 0;
  }

  out->info("Target database size: {}, type: {}", tdbr->getSize(), Parameters::getDbTypeName(targetSeqType));

  if (splitMode == Parameters::QUERY_DB_SPLIT) {
    // create the whole index table
    getIndexTable(out, 0, 0, tdbr->getSize());
  } else if (splitMode == Parameters::TARGET_DB_SPLIT) {
    sequenceLookup = NULL;
    indexTable = NULL;
  } else {
    out->failure("Invalid split mode was specified: {}", splitMode);
  }

  if (Parameters::isEqualDbtype(querySeqType, Parameters::DBTYPE_AMINO_ACIDS)) {
    kmerSubMat->alphabetSize = kmerSubMat->alphabetSize - 1;
    _2merSubMatrix = getScoreMatrix(out, *kmerSubMat, 2);
    _3merSubMatrix = getScoreMatrix(out, *kmerSubMat, 3);
    kmerSubMat->alphabetSize = alphabetSize;
  }
}

Prefiltering::~Prefiltering() {
  if (sameQTDB == false) {
    qdbr->close();
    delete qdbr;
  }

  if (indexTable != NULL) {
    delete indexTable;
  }

  if (sequenceLookup != NULL) {
    delete sequenceLookup;
  }

  tdbr->close();
  delete tdbr;

  if (templateDBIsIndex == true) {
    tidxdbr->close();
    delete tidxdbr;
  }

  if (templateDBIsIndex == false ||
      preloadMode == Parameters::PRELOAD_MODE_FREAD) {
    ExtendedSubstitutionMatrix::freeScoreMatrix(_3merSubMatrix);
    ExtendedSubstitutionMatrix::freeScoreMatrix(_2merSubMatrix);
  }

  if (kmerSubMat != ungappedSubMat) {
    delete ungappedSubMat;
  }
  delete kmerSubMat;
}

void Prefiltering::setupSplit(mmseqs_output* out, DBReader<unsigned int> &tdbr,
                              const int alphabetSize,
                              const unsigned int querySeqTyp, const int threads,
                              const bool templateDBIsIndex,
                              const size_t memoryLimit, const size_t qDbSize,
                              size_t &maxResListLen, int &kmerSize, int &split,
                              int &splitMode) {
  size_t memoryNeeded = estimateMemoryConsumption(
      1, tdbr.getSize(), tdbr.getAminoAcidDBSize(), maxResListLen, alphabetSize,
      kmerSize == 0 ?  // if auto detect kmerSize
          IndexTable::computeKmerSize(out, tdbr.getAminoAcidDBSize())
                    : kmerSize,
      querySeqTyp, threads);

  int optimalSplitMode = Parameters::TARGET_DB_SPLIT;
  if (memoryNeeded > 0.9 * memoryLimit) {
    if (splitMode == Parameters::QUERY_DB_SPLIT) {
      out->failure("--split-mode was set to query-split ({}) but memory limit requires target-split. Please use a computer with more main memory or run with default --split-mode setting.", Parameters::QUERY_DB_SPLIT);
    }
  } else {
#ifdef HAVE_MPI
    if (templateDBIsIndex) {
      optimalSplitMode = Parameters::TARGET_DB_SPLIT;
    } else {
      optimalSplitMode = Parameters::QUERY_DB_SPLIT;
    }
#else
    optimalSplitMode = Parameters::QUERY_DB_SPLIT;
#endif
  }

  // user split mode is legal and respected, only set this if we are in
  // automatic detection
  if (splitMode == Parameters::DETECT_BEST_DB_SPLIT) {
    splitMode = optimalSplitMode;
  }

  // ideally we always run without splitting
  size_t minimalNumSplits = 1;
  // get minimal number of splits in case of target split
  // we EXITed already in query split mode
  if (memoryNeeded > 0.9 * memoryLimit) {
    // memory is not enough to compute everything at once
    // TODO add PROFILE_STATE (just 6-mers)
    std::pair<int, int> splitSettings = Prefiltering::optimizeSplit(
        out, memoryLimit, &tdbr, alphabetSize, kmerSize, querySeqTyp, threads);
    if (splitSettings.second == -1) {
      out->failure("Cannot fit databases into {}. Please use a computer with more main memory.", ByteParser::format(out, memoryLimit));
    }
    if (kmerSize == 0) {
      // set k-mer based on aa size in database
      // if we have less than 10Mio * 335 amino acids use 6mers
      kmerSize = splitSettings.first;
    }
    minimalNumSplits = splitSettings.second;
  }

  size_t optimalNumSplits = minimalNumSplits;
  size_t sizeOfDbToSplit = tdbr.getSize();
  if (splitMode == Parameters::QUERY_DB_SPLIT) {
    sizeOfDbToSplit = qDbSize;
  }
#ifdef HAVE_MPI
  optimalNumSplits = std::max(
      static_cast<size_t>(std::max(MMseqsMPI::numProc, 1)), optimalNumSplits);
#endif
  optimalNumSplits = std::min(sizeOfDbToSplit, optimalNumSplits);

  // set the final number of splits
  if (split == 0) {
    if (optimalNumSplits > INT_MAX) {
      out->failure("optimalNumSplits is greater INT_MAX");
    }
    split = optimalNumSplits;
  }

  // templateDBIsIndex = false when called from indexdb
  if ((static_cast<size_t>(split) < minimalNumSplits) && (templateDBIsIndex)) {
    out->warn("split was set to {} but at least  {} are required. Please run with default paramerters", split, minimalNumSplits);
  } else if (static_cast<size_t>(split) > sizeOfDbToSplit) {
    out->failure("split was set to {} but the db to split has only {} sequences. Please run with default paramerters", split, sizeOfDbToSplit);
  }

  if (kmerSize == 0) {
    size_t aaSize = tdbr.getAminoAcidDBSize() / std::max(split, 1);
    kmerSize = IndexTable::computeKmerSize(out, aaSize);
  }

  // in TARGET_DB_SPLIT we have to reduce the number of prefilter hits can
  // produce, so that the merged database does not contain more than
  // maxResListLen
  if (splitMode == Parameters::TARGET_DB_SPLIT && split > 1) {
    size_t fourTimesStdDeviation = 4 * sqrt(static_cast<double>(maxResListLen) /
                                            static_cast<double>(split));
    maxResListLen = std::max(static_cast<size_t>(1),
                             (maxResListLen / split) + fourTimesStdDeviation);
  }

  if (split > 1) {
    out->info("{} split mode. Searching through {} splits", Parameters::getSplitModeName(splitMode), split);
  }

  size_t memoryNeededPerSplit = estimateMemoryConsumption(
      (splitMode == Parameters::TARGET_DB_SPLIT) ? split : 1, tdbr.getSize(),
      tdbr.getAminoAcidDBSize(), maxResListLen, alphabetSize, kmerSize,
      querySeqTyp, threads);

  out->info("Estimated memory consumption: {}", ByteParser::format(out, memoryNeededPerSplit));
  if (memoryNeededPerSplit > 0.9 * memoryLimit) {
    out->warn("Process needs more than {} main memory. Increase the size of --split or set it to 0 to automatically optimize target database split.", ByteParser::format(out, memoryLimit));
    if (templateDBIsIndex == true) {
      out->warn("Computed index is too large. Avoid using the index.");
    }
  }
}

void Prefiltering::mergeTargetSplits(
    mmseqs_output* out,
    const std::string &outDB, const std::string &outDBIndex,
    const std::vector<std::pair<std::string, std::string>> &fileNames,
    unsigned int threads) {
  // we assume that the hits are in the same order
  const size_t splits = fileNames.size();

  if (splits < 2) {
    DBReader<unsigned int>::moveDb(out, fileNames[0].first, outDB);
    out->info("No merging needed.");
    return;
  }

  Timer timer;
  out->info("Merging {} target splits to {}", splits, FileUtil::baseName(out, outDB));

  DBReader<unsigned int> reader1(out, fileNames[0].first.c_str(),
                                 fileNames[0].second.c_str(), 1,
                                 DBReader<unsigned int>::USE_INDEX);
  reader1.open(DBReader<unsigned int>::NOSORT);
  DBReader<unsigned int>::Index *index1 = reader1.getIndex();

  size_t totalSize = 0;
  for (size_t id = 0; id < reader1.getSize(); id++) {
    totalSize += index1[id].length;
  }
  for (size_t i = 1; i < splits; ++i) {
    DBReader<unsigned int> reader2(out, fileNames[i].first.c_str(),
                                   fileNames[i].second.c_str(), 1,
                                   DBReader<unsigned int>::USE_INDEX);
    reader2.open(DBReader<unsigned int>::NOSORT);
    DBReader<unsigned int>::Index *index2 = reader2.getIndex();
    size_t currOffset = 0;
    for (size_t id = 0; id < reader1.getSize(); id++) {
      // add length for file1 and file2 and subtract -1 for one null byte
      size_t seqLen = index1[id].length + index2[id].length - 1;
      totalSize += index2[id].length - 1;
      index1[id].length = seqLen;
      index1[id].offset = currOffset;
      currOffset += seqLen;
    }
    reader2.close();
  }
  reader1.setDataSize(totalSize);

  FILE **files = new FILE *[fileNames.size()];
  char **dataFile = new char *[fileNames.size()];
  size_t *dataFileSize = new size_t[fileNames.size()];
  size_t globalIdOffset = 0;
  for (size_t i = 0; i < splits; ++i) {
    files[i] = FileUtil::openFileOrDie(out, fileNames[i].first.c_str(), "r", true);
    dataFile[i] =
        static_cast<char *>(FileUtil::mmapFile(out, files[i], &dataFileSize[i]));
#ifdef HAVE_POSIX_MADVISE
    if (posix_madvise(dataFile[i], dataFileSize[i], POSIX_MADV_SEQUENTIAL) !=
        0) {
      out->error("posix_madvise returned an error {}", fileNames[i].first);
    }
#endif
  }
  out->info("Preparing offsets for merging: {}", timer.lap());
  // merge target splits data files and sort the hits at the same time
  // TODO: compressed?
  DBWriter writer(out, outDB.c_str(), outDBIndex.c_str(), threads, 0,
                  Parameters::DBTYPE_PREFILTER_RES);
  writer.open();

  Log::Progress progress(reader1.getSize());
#pragma omp parallel num_threads(threads)
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = static_cast<unsigned int>(omp_get_thread_num());
#endif
    std::string result;
    result.reserve(1024);
    std::vector<hit_t> hits;
    hits.reserve(300);
    char buffer[1024];
    size_t *currentDataFileOffset = new size_t[splits];
    memset(currentDataFileOffset, 0, sizeof(size_t) * splits);
    size_t currentId = __sync_fetch_and_add(&(globalIdOffset), 1);
    size_t prevId = 0;
    while (currentId < reader1.getSize()) {
      progress.updateProgress();
      for (size_t file = 0; file < splits; file++) {
        size_t tmpId = prevId;
        size_t pos;
        for (pos = currentDataFileOffset[file];
             pos < dataFileSize[file] && tmpId != currentId; pos++) {
          tmpId += (dataFile[file][pos] == '\0');
          currentDataFileOffset[file] = pos;
        }
        currentDataFileOffset[file] = pos;
        QueryMatcher::parsePrefilterHits(out, &dataFile[file][pos], hits);
      }
      if (hits.size() > 1) {
        SORT_SERIAL(hits.begin(), hits.end(), hit_t::compareHitsByScoreAndId);
      }
      for (size_t i = 0; i < hits.size(); ++i) {
        int len = QueryMatcher::prefilterHitToBuffer(buffer, hits[i]);
        result.append(buffer, len);
      }
      writer.writeData(result.c_str(), result.size(),
                       reader1.getDbKey(currentId), thread_idx);
      hits.clear();
      result.clear();
      prevId = currentId;
      currentId = __sync_fetch_and_add(&(globalIdOffset), 1);
    }

    delete[] currentDataFileOffset;
  }
  writer.close();
  reader1.close();

  for (size_t i = 0; i < splits; ++i) {
    DBReader<unsigned int>::removeDb(out, fileNames[i].first);
    FileUtil::munmapData(out, dataFile[i], dataFileSize[i]);
    if (fclose(files[i]) != 0) {
      out->failure("Cannot close file {}", fileNames[i].first);
    }
  }
  delete[] dataFile;
  delete[] dataFileSize;
  delete[] files;

  out->info("Time for merging target splits: {}", timer.lap());
}

ScoreMatrix Prefiltering::getScoreMatrix(mmseqs_output* out, const BaseMatrix &matrix,
                                         const size_t kmerSize) {
  if (templateDBIsIndex == true) {
    switch (kmerSize) {
      case 2:
        return PrefilteringIndexReader::get2MerScoreMatrix(tidxdbr,
                                                           preloadMode);
      case 3:
        return PrefilteringIndexReader::get3MerScoreMatrix(tidxdbr,
                                                           preloadMode);
      default:
        break;
    }
  }
  return ExtendedSubstitutionMatrix::calcScoreMatrix(out, matrix, kmerSize);
}

void Prefiltering::getIndexTable(mmseqs_output *out, int split, size_t dbFrom,
                                 size_t dbSize) {
  if (templateDBIsIndex == true) {
    indexTable =
        PrefilteringIndexReader::getIndexTable(out, split, tidxdbr, preloadMode);
    // only the ungapped alignment needs the sequence lookup, we can save quite
    // some memory here
    if (diagonalScoring) {
      sequenceLookup = PrefilteringIndexReader::getSequenceLookup(
          out, split, tidxdbr, preloadMode);
    }
  } else {
    Timer timer;

    Sequence tseq(out, maxSeqLen, targetSeqType, kmerSubMat, kmerSize, spacedKmer,
                  aaBiasCorrection, true, spacedKmerPattern);
    int localKmerThr =
        (Parameters::isEqualDbtype(querySeqType,
                                   Parameters::DBTYPE_HMM_PROFILE) ||
         Parameters::isEqualDbtype(querySeqType,
                                   Parameters::DBTYPE_PROFILE_STATE_PROFILE) ||
         Parameters::isEqualDbtype(querySeqType,
                                   Parameters::DBTYPE_NUCLEOTIDES) ||
         (Parameters::isEqualDbtype(targetSeqType,
                                    Parameters::DBTYPE_HMM_PROFILE) == false &&
          takeOnlyBestKmer == true))
            ? 0
            : kmerThr;

    // remove X or N for seeding
    int adjustAlphabetSize =
        (Parameters::isEqualDbtype(targetSeqType,
                                   Parameters::DBTYPE_NUCLEOTIDES) ||
         Parameters::isEqualDbtype(targetSeqType,
                                   Parameters::DBTYPE_AMINO_ACIDS))
            ? alphabetSize - 1
            : alphabetSize;
    indexTable = new IndexTable(out, adjustAlphabetSize, kmerSize, false);
    SequenceLookup **maskedLookup =
        maskMode == 1 || maskLowerCaseMode == 1 ? &sequenceLookup : NULL;
    SequenceLookup **unmaskedLookup = maskMode == 0 ? &sequenceLookup : NULL;

    out->info("Index table k-mer threshold: {} at k-mer size {}", localKmerThr, kmerSize);
    IndexBuilder::fillDatabase(
        out,
        indexTable, maskedLookup, unmaskedLookup, *kmerSubMat, &tseq, tdbr,
        dbFrom, dbFrom + dbSize, localKmerThr, maskMode, maskLowerCaseMode);

    // sequenceLookup has to be temporarily present to speed up masking
    // afterwards its not needed anymore without diagonal scoring
    if (diagonalScoring == false) {
      delete sequenceLookup;
      sequenceLookup = NULL;
    }

    indexTable->printStatistics(out, kmerSubMat->num2aa);
    tdbr->remapData();
    out->info("Time for index table init: {}", timer.lap());
  }
}

bool Prefiltering::isSameQTDB(mmseqs_output* out) {
  //  check if when qdb and tdb have the same name an index extension exists
  std::string check(targetDB);
  size_t pos = check.find(queryDB);
  int match = false;
  if (pos == 0) {
    check.replace(0, queryDB.length(), "");
    // TODO name changed to .idx
    PatternCompiler regex(out, "^\\.s?k[5-7]$");
    match = regex.isMatch(check.c_str());
  }
  // if no match found or two matches found (we want exactly one match)
  return (queryDB.compare(targetDB) == 0 || (match == true));
}

void Prefiltering::runAllSplits(mmseqs_output *out, const std::string &resultDB,
                                const std::string &resultDBIndex) {
  runSplits(out, resultDB, resultDBIndex, 0, splits, false);
}

#ifdef HAVE_MPI
void Prefiltering::runMpiSplits(mmseqs_output *out, const std::string &resultDB,
                                const std::string &resultDBIndex,
                                const std::string &localTmpPath,
                                const int runRandomId) {
  if (compressed == true && splitMode == Parameters::TARGET_DB_SPLIT) {
    out->warn("The output of the prefilter cannot be compressed during target split mode. Prefilter result will not be compressed.");
    compressed = false;
  }

  // if split size is great than nodes than we have to
  // distribute all splits equally over all nodes
  unsigned int *splitCntPerProc = new unsigned int[MMseqsMPI::numProc];
  memset(splitCntPerProc, 0, sizeof(unsigned int) * MMseqsMPI::numProc);
  for (int i = 0; i < splits; i++) {
    splitCntPerProc[i % MMseqsMPI::numProc] += 1;
  }

  size_t fromSplit = 0;
  for (int i = 0; i < MMseqsMPI::rank; i++) {
    fromSplit += splitCntPerProc[i];
  }

  size_t splitCount = splitCntPerProc[MMseqsMPI::rank];
  delete[] splitCntPerProc;

  // setting names in case of localTmp path
  std::string procTmpResultDB = localTmpPath;
  std::string procTmpResultDBIndex = localTmpPath;
  if (localTmpPath == "") {
    procTmpResultDB = resultDB;
    procTmpResultDBIndex = resultDBIndex;
  } else {
    procTmpResultDB = procTmpResultDB + "/" + FileUtil::baseName(out, resultDB);
    procTmpResultDBIndex =
        procTmpResultDBIndex + "/" + FileUtil::baseName(out, resultDBIndex);

    if (FileUtil::directoryExists(out, localTmpPath.c_str()) == false) {
      out->info("Local tmp dir {} does not exist or is not a directory", localTmpPath);
      if (FileUtil::makeDir(out, localTmpPath.c_str()) == false) {
        out->failure("Cannot create local tmp dir {}", localTmpPath);
      } else {
        out->info("Created local tmp dir {}", localTmpPath);
      }
    }
  }

  std::pair<std::string, std::string> result = Util::createTmpFileNames(
      procTmpResultDB, procTmpResultDBIndex, MMseqsMPI::rank + runRandomId);
  bool merge = (splitMode == Parameters::QUERY_DB_SPLIT);

  int hasResult = runSplits(out, result.first, result.second, fromSplit,
                            splitCount, merge) == true
                      ? 1
                      : 0;

  if (localTmpPath != "") {
    std::pair<std::string, std::string> resultShared =
        Util::createTmpFileNames(resultDB, resultDBIndex, MMseqsMPI::rank);
    // moveDb takes care if file doesn't exist
    DBReader<unsigned int>::moveDb(result.first, resultShared.first);
  }

  int *results = NULL;
  if (MMseqsMPI::isMaster()) {
    results = new int[MMseqsMPI::numProc]();
  }

  MPI_Gather(&hasResult, 1, MPI_INT, results, 1, MPI_INT, MMseqsMPI::MASTER,
             MPI_COMM_WORLD);
  if (MMseqsMPI::isMaster()) {
    // gather does not write the result of the master into the array
    results[MMseqsMPI::MASTER] = hasResult;

    std::vector<std::pair<std::string, std::string>> splitFiles;
    for (int i = 0; i < MMseqsMPI::numProc; ++i) {
      if (results[i] == 1) {
        std::pair<std::string, std::string> resultOfRanki =
            Util::createTmpFileNames(resultDB, resultDBIndex, i);
        splitFiles.push_back(
            std::make_pair(resultOfRanki.first, resultOfRanki.second));
      }
    }

    if (splitFiles.size() > 0) {
      // merge output databases
      mergePrefilterSplits(resultDB, resultDBIndex, splitFiles);
    } else {
      out->failure("Aborting. No results were computed");
    }

    delete[] results;
  }
}
#endif

int Prefiltering::runSplits(mmseqs_output *out, const std::string &resultDB,
                            const std::string &resultDBIndex, size_t fromSplit,
                            size_t splitProcessCount, bool merge) {
  if (fromSplit + splitProcessCount > static_cast<size_t>(splits)) {
    out->failure("Start split {} plus split count {} cannot be larger than splits {}", fromSplit, splitProcessCount, splits);
  }

  size_t freeSpace =
      FileUtil::getFreeSpace(out, FileUtil::dirName(out, resultDB).c_str());
  size_t estimatedHDDMemory =
      estimateHDDMemoryConsumption(qdbr->getSize(), maxResListLen);
  if (freeSpace < estimatedHDDMemory) {
    std::string freeSpaceToPrint = ByteParser::format(out, freeSpace);
    std::string estimatedHDDMemoryToPrint =
        ByteParser::format(out, estimatedHDDMemory);
    out->warn("Hard disk might not have enough free space ({} left). The prefilter result might need up to {}.", freeSpaceToPrint, estimatedHDDMemoryToPrint);
  }

  bool hasResult = false;
  if (splitProcessCount > 1) {
    if (compressed == true && splitMode == Parameters::TARGET_DB_SPLIT) {
      out->warn("The output of the prefilter cannot be compressed during target split mode. Prefilter result will not be compressed.");
      compressed = false;
    }
    // splits template database into x sequence steps
    std::vector<std::pair<std::string, std::string>> splitFiles;
    for (size_t i = fromSplit; i < (fromSplit + splitProcessCount); i++) {
      std::pair<std::string, std::string> filenamePair =
          Util::createTmpFileNames(resultDB, resultDBIndex, i);
      if (runSplit(out, filenamePair.first.c_str(), filenamePair.second.c_str(),
                   i, merge)) {
        splitFiles.push_back(filenamePair);
      }
    }
    if (splitFiles.size() > 0) {
      mergePrefilterSplits(out, resultDB, resultDBIndex, splitFiles);
      if (splitFiles.size() > 1) {
        DBReader<unsigned int> resultReader(
            out,
            resultDB.c_str(), resultDBIndex.c_str(), threads,
            DBReader<unsigned int>::USE_INDEX |
                DBReader<unsigned int>::USE_DATA);
        resultReader.open(DBReader<unsigned int>::NOSORT);
        resultReader.readMmapedDataInMemory();
        const std::pair<std::string, std::string> tempDb =
            Util::databaseNames(resultDB + "_tmp");
        DBWriter resultWriter(out, tempDb.first.c_str(), tempDb.second.c_str(),
                              threads, compressed,
                              Parameters::DBTYPE_PREFILTER_RES);
        resultWriter.open();
        resultWriter.sortDatafileByIdOrder(resultReader);
        resultWriter.close(true);
        resultReader.close();
        DBReader<unsigned int>::removeDb(out, resultDB);
        DBReader<unsigned int>::moveDb(out, tempDb.first, resultDB);
      }
      hasResult = true;
    }
  } else if (splitProcessCount == 1) {
    if (runSplit(out, resultDB.c_str(), resultDBIndex.c_str(), fromSplit,
                 merge)) {
      hasResult = true;
    }
  }

  return hasResult;
}

bool Prefiltering::runSplit(mmseqs_output *out, const std::string &resultDB,
                            const std::string &resultDBIndex, size_t split,
                            bool merge) {
  out->info("Process prefiltering step {} of {}", split+1, splits);

  size_t dbFrom = 0;
  size_t dbSize = tdbr->getSize();
  size_t queryFrom = 0;
  size_t querySize = qdbr->getSize();

  // create index table based on split parameter
  if (splitMode == Parameters::TARGET_DB_SPLIT) {
    tdbr->decomposeDomainByAminoAcid(split, splits, &dbFrom, &dbSize);
    if (dbSize == 0) {
      return false;
    }

    if (indexTable != NULL) {
      delete indexTable;
      indexTable = NULL;
    }

    if (sequenceLookup != NULL) {
      delete sequenceLookup;
      sequenceLookup = NULL;
    }

    getIndexTable(out, split, dbFrom, dbSize);
  } else if (splitMode == Parameters::QUERY_DB_SPLIT) {
    qdbr->decomposeDomainByAminoAcid(split, splits, &queryFrom, &querySize);
    if (querySize == 0) {
      return false;
    }
  }

  out->info("k-mer similarity threshold: {}", kmerThr);

  double kmersPerPos = 0;
  size_t dbMatches = 0;
  size_t doubleMatches = 0;
  size_t querySeqLenSum = 0;
  size_t resSize = 0;
  size_t realResSize = 0;
  size_t diagonalOverflow = 0;
  size_t trancatedCounter = 0;
  size_t totalQueryDBSize = querySize;

  unsigned int localThreads = 1;
#ifdef OPENMP
  localThreads = std::min((unsigned int)threads, (unsigned int)querySize);
#endif

  DBWriter tmpDbw(out, resultDB.c_str(), resultDBIndex.c_str(), localThreads,
                  compressed, Parameters::DBTYPE_PREFILTER_RES);
  tmpDbw.open();

  // init all thread-specific data structures
  char *notEmpty = new char[querySize];
  memset(notEmpty, 0, querySize * sizeof(char));  // init notEmpty

  std::list<int> **reslens = new std::list<int> *[localThreads];
  for (unsigned int i = 0; i < localThreads; ++i) {
    reslens[i] = new std::list<int>();
  }

  out->info("Starting prefiltering scores calculation (step {} of {})", split+1, splits);
  out->info("Query db start {} to {}", queryFrom + 1, queryFrom + querySize);
  out->info("Target db start {} to {}", dbFrom + 1, dbFrom + dbSize);

  Log::Progress progress(querySize);

#pragma omp parallel num_threads(localThreads)
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = static_cast<unsigned int>(omp_get_thread_num());
#endif
    Sequence seq(out, qdbr->getMaxSeqLen(), querySeqType, kmerSubMat, kmerSize,
                 spacedKmer, aaBiasCorrection, true, spacedKmerPattern);
    QueryMatcher matcher(out, indexTable, sequenceLookup, kmerSubMat, ungappedSubMat,
                         kmerThr, kmerSize, dbSize,
                         std::max(tdbr->getMaxSeqLen(), qdbr->getMaxSeqLen()),
                         maxResListLen, aaBiasCorrection, diagonalScoring,
                         minDiagScoreThr, takeOnlyBestKmer);

    if (seq.profile_matrix != NULL) {
      matcher.setProfileMatrix(seq.profile_matrix);
    } else if (_3merSubMatrix.isValid() && _2merSubMatrix.isValid()) {
      matcher.setSubstitutionMatrix(&_3merSubMatrix, &_2merSubMatrix);
    } else {
      matcher.setSubstitutionMatrix(NULL, NULL);
    }

    char buffer[128];
    std::string result;
    result.reserve(1000000);

#pragma omp for schedule(dynamic, 2) reduction (+: kmersPerPos, resSize, dbMatches, doubleMatches, querySeqLenSum, diagonalOverflow, trancatedCounter)
    for (size_t id = queryFrom; id < queryFrom + querySize; id++) {
      progress.updateProgress();
      // get query sequence
      char *seqData = qdbr->getData(id, thread_idx);
      unsigned int qKey = qdbr->getDbKey(id);
      seq.mapSequence(id, qKey, seqData, qdbr->getSeqLen(id));
      size_t targetSeqId = UINT_MAX;
      if (sameQTDB || includeIdentical) {
        targetSeqId = tdbr->getId(seq.getDbKey());
        // only the corresponding split should include the id (hack for the
        // hack)
        if (targetSeqId >= dbFrom && targetSeqId < (dbFrom + dbSize) &&
            targetSeqId != UINT_MAX) {
          targetSeqId = targetSeqId - dbFrom;
          if (targetSeqId > tdbr->getSize()) {
            out->failure("targetSeqId: {} > target database size: {}", targetSeqId, tdbr->getSize());
          }
        } else {
          targetSeqId = UINT_MAX;
        }
      }
      // calculate prefiltering results
      std::pair<hit_t *, size_t> prefResults =
          matcher.matchQuery(&seq, targetSeqId);
      size_t resultSize = prefResults.second;
      const float queryLength = static_cast<float>(qdbr->getSeqLen(id));
      for (size_t i = 0; i < resultSize; i++) {
        hit_t *res = prefResults.first + i;
        // correct the 0 indexed sequence id again to its real identifier
        size_t targetSeqId1 = res->seqId + dbFrom;
        // replace id with key
        res->seqId = tdbr->getDbKey(targetSeqId1);
        if (UNLIKELY(targetSeqId1 >= tdbr->getSize())) {
          out->warn("Wrong prefiltering result for query: {} -> {}  (score: {})", qdbr->getDbKey(id), targetSeqId1, res->prefScore);
        }

        // TODO: check if this should happen when diagonalScoring == false
        if (covThr > 0.0 && (covMode == Parameters::COV_MODE_BIDIRECTIONAL ||
                             covMode == Parameters::COV_MODE_QUERY ||
                             covMode == Parameters::COV_MODE_LENGTH_SHORTER)) {
          const float targetLength =
              static_cast<float>(tdbr->getSeqLen(targetSeqId1));
          if (Util::canBeCovered(covThr, covMode, queryLength, targetLength) ==
              false) {
            continue;
          }
        }

        // write prefiltering results to a string
        int len = QueryMatcher::prefilterHitToBuffer(buffer, *res);
        result.append(buffer, len);
      }
      tmpDbw.writeData(result.c_str(), result.length(), qKey, thread_idx);
      result.clear();

      // update statistics counters
      if (resultSize != 0) {
        notEmpty[id - queryFrom] = 1;
      }

      if (Log::debugLevel >= Log::INFO) {
        kmersPerPos += matcher.getStatistics()->kmersPerPos;
        dbMatches += matcher.getStatistics()->dbMatches;
        doubleMatches += matcher.getStatistics()->doubleMatches;
        querySeqLenSum += seq.L;
        diagonalOverflow += matcher.getStatistics()->diagonalOverflow;
        trancatedCounter += matcher.getStatistics()->truncated;
        resSize += resultSize;
        realResSize += std::min(resultSize, maxResListLen);
        reslens[thread_idx]->emplace_back(resultSize);
      }
    }  // step end
  }

  if (Log::debugLevel >= Log::INFO) {
    statistics_t stats(kmersPerPos / static_cast<double>(totalQueryDBSize),
                       dbMatches / totalQueryDBSize,
                       doubleMatches / totalQueryDBSize, querySeqLenSum,
                       diagonalOverflow, resSize / totalQueryDBSize,
                       trancatedCounter);

    size_t empty = 0;
    for (size_t id = 0; id < querySize; id++) {
      if (notEmpty[id] == 0) {
        empty++;
      }
    }

    printStatistics(out, stats, reslens, localThreads, empty, maxResListLen);
  }

  if (splitMode == Parameters::TARGET_DB_SPLIT && splits == 1) {
#ifdef HAVE_MPI
    // if a mpi rank processed a single split, it must have it merged before all
    // ranks can be united
    tmpDbw.close(true);
#else
    tmpDbw.close(merge);
#endif
  } else {
    tmpDbw.close(merge);
  }

  // sort by ids
  // needed to speed up merge later on
  // sorts this datafile according to the index file
  if (splitMode == Parameters::TARGET_DB_SPLIT && splits > 1) {
    // free memory early since the merge might need quite a bit of memory
    if (indexTable != NULL) {
      delete indexTable;
      indexTable = NULL;
    }
    if (sequenceLookup != NULL) {
      delete sequenceLookup;
      sequenceLookup = NULL;
    }
    DBReader<unsigned int> resultReader(
        out,
        tmpDbw.getDataFileName(), tmpDbw.getIndexFileName(), threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    resultReader.open(DBReader<unsigned int>::NOSORT);
    resultReader.readMmapedDataInMemory();
    const std::pair<std::string, std::string> tempDb =
        Util::databaseNames((resultDB + "_tmp"));
    DBWriter resultWriter(out, tempDb.first.c_str(), tempDb.second.c_str(),
                          localThreads, compressed,
                          Parameters::DBTYPE_PREFILTER_RES);
    resultWriter.open();
    resultWriter.sortDatafileByIdOrder(resultReader);
    resultWriter.close(true);
    resultReader.close();
    DBReader<unsigned int>::removeDb(out, resultDB);
    DBReader<unsigned int>::moveDb(out, tempDb.first, resultDB);
  }

  for (unsigned int i = 0; i < localThreads; i++) {
    reslens[i]->clear();
    delete reslens[i];
  }
  delete[] reslens;
  delete[] notEmpty;

  return true;
}

void Prefiltering::printStatistics(mmseqs_output* out, const statistics_t &stats,
                                   std::list<int> **reslens,
                                   unsigned int resLensSize, size_t empty,
                                   size_t maxResults) {
  // sort and merge the result list lengths (for median calculation)
  reslens[0]->sort();
  for (unsigned int i = 1; i < resLensSize; i++) {
    reslens[i]->sort();
    reslens[0]->merge(*reslens[i]);
  }

  out->info("{} k-mers per position", stats.kmersPerPos);
  out->info("{} DB matches per sequence", stats.dbMatches);
  out->info("{} overflows", stats.diagonalOverflow);
  out->info("{} queries produce too many hits (truncated result)", stats.truncated);
  out->info("{} sequences passed prefiltering per query sequence", stats.resultsPassedPrefPerSeq);

  if (stats.resultsPassedPrefPerSeq > maxResults) {
    out->warn("(ATTENTION: max. {} best scoring sequences were written to the output prefiltering database)", maxResults);
  }

  size_t mid = reslens[0]->size() / 2;
  std::list<int>::iterator it = reslens[0]->begin();
  std::advance(it, mid);

  out->info("{} median result list length", *it);
  out->info("{} sequences with 0 size result lists", empty);
}

BaseMatrix *Prefiltering::getSubstitutionMatrix(
    mmseqs_output* out,
    const MultiParam<char *> &scoringMatrixFile, MultiParam<int> alphabetSize,
    float bitFactor, bool profileState, bool isNucl) {
  BaseMatrix *subMat;

  if (isNucl) {
    subMat =
        new NucleotideMatrix(out, scoringMatrixFile.nucleotides, bitFactor, 0.0);
  } else if (alphabetSize.aminoacids < 21) {
    SubstitutionMatrix sMat(out, scoringMatrixFile.aminoacids, bitFactor, -0.2f);
    subMat = new ReducedMatrix(out, sMat.probMatrix, sMat.subMatrixPseudoCounts,
                               sMat.aa2num, sMat.num2aa, sMat.alphabetSize,
                               alphabetSize.aminoacids, bitFactor);
  } else if (profileState == true) {
    SubstitutionMatrix sMat(out, scoringMatrixFile.aminoacids, bitFactor, -0.2f);
    subMat = new SubstitutionMatrixProfileStates(
        out,
        sMat.matrixName, sMat.probMatrix, sMat.pBack,
        sMat.subMatrixPseudoCounts, bitFactor, 0.0, 8);
  } else {
    subMat =
        new SubstitutionMatrix(out, scoringMatrixFile.aminoacids, bitFactor, -0.2f);
  }
  return subMat;
}

void Prefiltering::mergePrefilterSplits(
    mmseqs_output* out,
    const std::string &outDB, const std::string &outDBIndex,
    const std::vector<std::pair<std::string, std::string>> &splitFiles) {
  if (splitMode == Parameters::TARGET_DB_SPLIT) {
    mergeTargetSplits(out, outDB, outDBIndex, splitFiles, threads);
  } else if (splitMode == Parameters::QUERY_DB_SPLIT) {
    DBWriter::mergeResults(out, outDB, outDBIndex, splitFiles);
  }
}

int Prefiltering::getKmerThreshold(mmseqs_output* out, const float sensitivity,
                                   const bool isProfile, const int kmerScore,
                                   const int kmerSize) {
  double kmerThrBest = kmerScore;
  if (kmerScore == INT_MAX) {
    if (isProfile) {
      if (kmerSize == 5) {
        float base = 140.75;
        kmerThrBest = base - (sensitivity * 8.75);
      } else if (kmerSize == 6) {
        float base = 155.75;
        kmerThrBest = base - (sensitivity * 8.75);
      } else if (kmerSize == 7) {
        float base = 171.75;
        kmerThrBest = base - (sensitivity * 9.75);
      } else {
        out->failure("The k-mer size {} is not valid.", kmerSize);
      }
    } else {
      if (kmerSize == 5) {
        float base = 160.75;
        kmerThrBest = base - (sensitivity * 12.75);
      } else if (kmerSize == 6) {
        float base = 163.2;
        kmerThrBest = base - (sensitivity * 8.917);
      } else if (kmerSize == 7) {
        float base = 186.15;
        kmerThrBest = base - (sensitivity * 11.22);
      } else {
        out->failure("The k-mer size {} is not valid.", kmerSize);
      }
    }
  }
  return static_cast<int>(kmerThrBest);
}

size_t Prefiltering::estimateMemoryConsumption(
    int split, size_t dbSize, size_t resSize, size_t maxResListLen,
    int alphabetSize, int kmerSize, unsigned int querySeqType, int threads) {
  // for each residue in the database we need 7 byte
  size_t dbSizeSplit = (dbSize) / split;
  size_t residueSize = (resSize / split * 7);
  // 21^7 * pointer size is needed for the index
  size_t indexTableSize =
      static_cast<size_t>(pow(alphabetSize, kmerSize)) * sizeof(size_t);
  // memory needed for the threads
  // This memory is an approx. for Countint32Array and QueryTemplateLocalFast
  size_t threadSize =
      threads *
      ((dbSizeSplit * 2 *
        sizeof(IndexEntryLocal))                // databaseHits in QueryMatcher
       + (dbSizeSplit * sizeof(CounterResult))  // databaseHits in QueryMatcher
       + (maxResListLen * sizeof(hit_t)) +
       (dbSizeSplit * 2 * sizeof(CounterResult) *
        2)  // BINS * binSize, (binSize = dbSize * 2 / BINS)
            // 2 is a security factor the size can increase during run
      );
  size_t dbReaderSize = dbSize * (sizeof(DBReader<unsigned int>::Index) +
                                  sizeof(unsigned int));  // DB index size

  // extended matrix
  size_t extendedMatrix = 0;
  if (Parameters::isEqualDbtype(querySeqType, Parameters::DBTYPE_AMINO_ACIDS)) {
    extendedMatrix = sizeof(std::pair<short, unsigned int>) *
                     static_cast<size_t>(pow(pow(alphabetSize, 3), 2));
    extendedMatrix +=
        sizeof(std::pair<short, unsigned int>) * pow(pow(alphabetSize, 2), 2);
  }
  // some memory needed to keep the index, ....
  size_t background = dbSize * 22;
  // return result in bytes
  return residueSize + indexTableSize + threadSize + background +
         extendedMatrix + dbReaderSize;
}

size_t Prefiltering::estimateHDDMemoryConsumption(size_t dbSize,
                                                  size_t maxResListLen) {
  // 21 bytes is roughly the size of an entry
  // 2x because the merge doubles the hdd demand
  return 2 * (21 * dbSize * maxResListLen);
}

std::pair<int, int> Prefiltering::optimizeSplit(
    mmseqs_output* out,
    size_t totalMemoryInByte, DBReader<unsigned int> *tdbr, int alphabetSize,
    int externalKmerSize, unsigned int querySeqType, unsigned int threads) {
  int startKmerSize = (externalKmerSize == 0) ? 6 : externalKmerSize;
  int endKmerSize = (externalKmerSize == 0) ? 7 : externalKmerSize;

  if (Parameters::isEqualDbtype(querySeqType, Parameters::DBTYPE_NUCLEOTIDES)) {
    startKmerSize = (externalKmerSize == 0) ? 14 : externalKmerSize;
    endKmerSize = (externalKmerSize == 0) ? 15 : externalKmerSize;
  }

  for (int optKmerSize = endKmerSize; optKmerSize >= startKmerSize;
       optKmerSize--) {
    size_t aaUpperBoundForKmerSize = (SIZE_MAX - 1);
    if (externalKmerSize == 0) {
      if (Parameters::isEqualDbtype(querySeqType,
                                    Parameters::DBTYPE_NUCLEOTIDES)) {
        aaUpperBoundForKmerSize =
            IndexTable::getUpperBoundNucCountForKmerSize(out, optKmerSize);
      } else {
        aaUpperBoundForKmerSize =
            IndexTable::getUpperBoundAACountForKmerSize(out, optKmerSize);
      }
    }
    for (int optSplit = 1; optSplit < 1000; optSplit++) {
      if ((tdbr->getAminoAcidDBSize() / optSplit) < aaUpperBoundForKmerSize) {
        size_t neededSize = estimateMemoryConsumption(
            optSplit, tdbr->getSize(), tdbr->getAminoAcidDBSize(), 0,
            alphabetSize, optKmerSize, querySeqType, threads);
        if (neededSize < 0.9 * totalMemoryInByte) {
          return std::make_pair(optKmerSize, optSplit);
        }
      }
    }
  }

  return std::make_pair(-1, -1);
}
