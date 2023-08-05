#include <mmseqs/prefiltering/indexBuilder.h>
#include <mmseqs/commons/tantan.h>

#ifdef OPENMP
#include <omp.h>
#endif

char *getScoreLookup(mmseqs_output* out, BaseMatrix &matrix) {
  char *idScoreLookup = NULL;
  idScoreLookup = new char[matrix.alphabetSize];
  for (int aa = 0; aa < matrix.alphabetSize; aa++) {
    short score = matrix.subMatrix[aa][aa];
    if (score > SCHAR_MAX || score < SCHAR_MIN) {
      out->warn( "Truncating substitution matrix diagonal score");
    }
    idScoreLookup[aa] = (char)score;
  }
  return idScoreLookup;
}

class DbInfo {
 public:
  DbInfo(size_t dbFrom, size_t dbTo, unsigned int effectiveKmerSize,
         DBReader<unsigned int> &reader) {
    tableSize = 0;
    aaDbSize = 0;
    size_t dbSize = dbTo - dbFrom;
    sequenceOffsets = new size_t[dbSize];
    sequenceOffsets[0] = 0;
    for (size_t id = dbFrom; id < dbTo; id++) {
      const int seqLen = reader.getSeqLen(id);
      aaDbSize += seqLen;
      size_t idFromNull = (id - dbFrom);
      if (id < dbTo - 1) {
        sequenceOffsets[idFromNull + 1] = sequenceOffsets[idFromNull] + seqLen;
      }
      if (Util::overlappingKmers(seqLen, effectiveKmerSize > 0)) {
        tableSize += 1;
      }
    }
  }

  ~DbInfo() { delete[] sequenceOffsets; }

  size_t tableSize;
  size_t aaDbSize;
  size_t *sequenceOffsets;
};

void IndexBuilder::fillDatabase(mmseqs_output* out, IndexTable *indexTable,
                                SequenceLookup **maskedLookup,
                                SequenceLookup **unmaskedLookup,
                                BaseMatrix &subMat, Sequence *seq,
                                DBReader<unsigned int> *dbr, size_t dbFrom,
                                size_t dbTo, int kmerThr, bool mask,
                                bool maskLowerCaseMode) {
  out->info("Index table: counting k-mers");

  const bool isProfile = Parameters::isEqualDbtype(
      seq->getSeqType(), Parameters::DBTYPE_HMM_PROFILE);

  dbTo = std::min(dbTo, dbr->getSize());
  size_t dbSize = dbTo - dbFrom;
  DbInfo *info = new DbInfo(dbFrom, dbTo, seq->getEffectiveKmerSize(), *dbr);

  SequenceLookup *sequenceLookup;
  if (unmaskedLookup != NULL && maskedLookup == NULL) {
    *unmaskedLookup = new SequenceLookup(out, dbSize, info->aaDbSize);
    sequenceLookup = *unmaskedLookup;
  } else if (unmaskedLookup == NULL && maskedLookup != NULL) {
    *maskedLookup = new SequenceLookup(out, dbSize, info->aaDbSize);
    sequenceLookup = *maskedLookup;
  } else if (unmaskedLookup != NULL && maskedLookup != NULL) {
    *unmaskedLookup = new SequenceLookup(out, dbSize, info->aaDbSize);
    *maskedLookup = new SequenceLookup(out, dbSize, info->aaDbSize);
    sequenceLookup = *maskedLookup;
  } else {
    out->failure("Failed assertion that should never fail during database filling.");
  }

  // need to prune low scoring k-mers through masking
  ProbabilityMatrix *probMatrix = NULL;
  if (maskedLookup != NULL) {
    probMatrix = new ProbabilityMatrix(subMat);
  }

  // identical scores for memory reduction code
  char *idScoreLookup = NULL;
  if (Parameters::isEqualDbtype(
          seq->getSeqType(), Parameters::DBTYPE_PROFILE_STATE_SEQ) == false) {
    idScoreLookup = getScoreLookup(out, subMat);
  }
  Log::Progress progress(dbTo - dbFrom);

  size_t maskedResidues = 0;
  size_t totalKmerCount = 0;
#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = static_cast<unsigned int>(omp_get_thread_num());
#endif

    Indexer idxer(out, static_cast<unsigned int>(indexTable->getAlphabetSize()),
                  seq->getKmerSize());
    Sequence s(out, seq->getMaxLen(), seq->getSeqType(), &subMat, seq->getKmerSize(),
               seq->isSpaced(), false, true, seq->getUserSpacedKmerPattern());

    KmerGenerator *generator = NULL;
    if (isProfile) {
      generator = new KmerGenerator(out, seq->getKmerSize(),
                                    indexTable->getAlphabetSize(), kmerThr);
      generator->setDivideStrategy(s.profile_matrix);
    }

    unsigned int *buffer = static_cast<unsigned int *>(
        malloc(seq->getMaxLen() * sizeof(unsigned int)));
    unsigned int bufferSize = seq->getMaxLen();
#pragma omp for schedule(dynamic, 100) reduction(+:totalKmerCount, maskedResidues)
    for (size_t id = dbFrom; id < dbTo; id++) {
      progress.updateProgress();

      s.resetCurrPos();
      char *seqData = dbr->getData(id, thread_idx);
      unsigned int qKey = dbr->getDbKey(id);

      s.mapSequence(id - dbFrom, qKey, seqData, dbr->getSeqLen(id));
      if (s.getMaxLen() >= bufferSize) {
        buffer = static_cast<unsigned int *>(
            realloc(buffer, s.getMaxLen() * sizeof(unsigned int)));
        bufferSize = seq->getMaxLen();
      }
      // count similar or exact k-mers based on sequence type
      if (isProfile) {
        // Find out if we should also mask profiles
        totalKmerCount += indexTable->addSimilarKmerCount(&s, generator);
        (*unmaskedLookup)
            ->addSequence(s.numConsensusSequence, s.L, id - dbFrom,
                          info->sequenceOffsets[id - dbFrom]);
      } else {
        // Do not mask if column state sequences are used
        if (unmaskedLookup != NULL) {
          (*unmaskedLookup)
              ->addSequence(s.numSequence, s.L, id - dbFrom,
                            info->sequenceOffsets[id - dbFrom]);
        }
        if (mask == true) {
          // s.print();
          maskedResidues += tantan::maskSequences(
              (char *)s.numSequence, (char *)(s.numSequence + s.L),
              50 /*options.maxCycleLength*/, probMatrix->probMatrixPointers,
              0.005 /*options.repeatProb*/, 0.05 /*options.repeatEndProb*/,
              0.9 /*options.repeatOffsetProbDecay*/, 0, 0,
              0.9 /*options.minMaskProb*/, probMatrix->hardMaskTable);
        }

        if (maskLowerCaseMode == true &&
            (Parameters::isEqualDbtype(s.getSequenceType(),
                                       Parameters::DBTYPE_AMINO_ACIDS) ||
             Parameters::isEqualDbtype(s.getSequenceType(),
                                       Parameters::DBTYPE_NUCLEOTIDES))) {
          const char *charSeq = s.getSeqData();
          unsigned char maskLetter = subMat.aa2num[static_cast<int>('X')];
          for (int i = 0; i < s.L; i++) {
            bool isLowerCase = (islower(charSeq[i]));
            maskedResidues += isLowerCase;
            s.numSequence[i] = isLowerCase ? maskLetter : s.numSequence[i];
          }
        }
        if (maskedLookup != NULL) {
          (*maskedLookup)
              ->addSequence(s.numSequence, s.L, id - dbFrom,
                            info->sequenceOffsets[id - dbFrom]);
        }

        totalKmerCount += indexTable->addKmerCount(&s, &idxer, buffer, kmerThr,
                                                   idScoreLookup);
      }
    }

    free(buffer);

    if (generator != NULL) {
      delete generator;
    }
  }

  if (probMatrix != NULL) {
    delete probMatrix;
  }

  out->info("Index table: Masked residues: {}", maskedResidues);
  if (totalKmerCount == 0) {
    if (!maskedResidues) {
       out->failure("No k-mer could be extracted for the database {}. Maybe the sequences length is less than 14 residues.", dbr->getDataFileName());
    } else {
       out->failure("No k-mer could be extracted for the database {}. Maybe the sequences length is less than 14 residues or contains only low complexity regions. Use mask=False to deactivate the low complexity filter.", dbr->getDataFileName());
    }
  }

  dbr->remapData();

  indexTable->initMemory(info->tableSize);
  indexTable->init();

  delete info;
  Log::Progress progress2(dbTo - dbFrom);

  out->info("Index table: fill");
#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = static_cast<unsigned int>(omp_get_thread_num());
#endif
    Sequence s(out, seq->getMaxLen(), seq->getSeqType(), &subMat, seq->getKmerSize(),
               seq->isSpaced(), false, true, seq->getUserSpacedKmerPattern());
    Indexer idxer(out, static_cast<unsigned int>(indexTable->getAlphabetSize()),
                  seq->getKmerSize());
    IndexEntryLocalTmp *buffer = static_cast<IndexEntryLocalTmp *>(
        malloc(seq->getMaxLen() * sizeof(IndexEntryLocalTmp)));
    size_t bufferSize = seq->getMaxLen();
    KmerGenerator *generator = NULL;
    if (isProfile) {
      generator = new KmerGenerator(out, seq->getKmerSize(),
                                    indexTable->getAlphabetSize(), kmerThr);
      generator->setDivideStrategy(s.profile_matrix);
    }

#pragma omp for schedule(dynamic, 100)
    for (size_t id = dbFrom; id < dbTo; id++) {
      s.resetCurrPos();
      progress2.updateProgress();

      unsigned int qKey = dbr->getDbKey(id);
      if (isProfile) {
        s.mapSequence(id - dbFrom, qKey, dbr->getData(id, thread_idx),
                      dbr->getSeqLen(id));
        indexTable->addSimilarSequence(&s, generator, &buffer, bufferSize,
                                       &idxer);
      } else {
        s.mapSequence(id - dbFrom, qKey,
                      sequenceLookup->getSequence(id - dbFrom));
        indexTable->addSequence(&s, &idxer, &buffer, bufferSize, kmerThr,
                                idScoreLookup);
      }
    }

    if (generator != NULL) {
      delete generator;
    }

    free(buffer);
  }
  if (idScoreLookup != NULL) {
    delete[] idScoreLookup;
  }
  indexTable->revertPointer();
  indexTable->sortDBSeqLists();
}
