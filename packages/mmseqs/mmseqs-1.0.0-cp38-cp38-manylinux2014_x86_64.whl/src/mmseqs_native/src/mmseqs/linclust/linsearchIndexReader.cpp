//
// Created by Martin Steinegger on 2019-01-04.
//
#include <mmseqs/linclust/linsearchIndexReader.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/linclust/kmerIndex.h>
#include <mmseqs/commons/nucleotideMatrix.h>
#include <mmseqs/prefiltering/prefilteringIndexReader.h>
#include <mmseqs/prefiltering/reducedMatrix.h>
#include <mmseqs/commons/substitutionMatrix.h>
#include <mmseqs/commons/timer.h>
#include <mmseqs/linclust/kmersearch.h>
#ifndef SIZE_T_MAX
#define SIZE_T_MAX ((size_t)-1)
#endif

template <int TYPE>
size_t LinsearchIndexReader::pickCenterKmer(mmseqs_output* out, KmerPosition<short> *hashSeqPair,
                                            size_t splitKmerCount) {
  size_t writePos = 0;
  size_t prevHash = hashSeqPair[0].kmer;
  if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
    prevHash = BIT_SET(prevHash, 63);
  }
  size_t prevHashStart = 0;
  size_t prevSetSize = 0;
  for (size_t elementIdx = 0; elementIdx < splitKmerCount + 1; elementIdx++) {
    size_t currKmer = hashSeqPair[elementIdx].kmer;
    if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
      currKmer = BIT_SET(currKmer, 63);
    }
    if (prevHash != currKmer) {
      size_t indexToPick = 0;
      size_t randIdx = prevHashStart + indexToPick;
      size_t kmer = hashSeqPair[randIdx].kmer;
      if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
        kmer = BIT_SET(hashSeqPair[randIdx].kmer, 63);
      }
      // remove singletones from set
      if (kmer != SIZE_T_MAX) {
        hashSeqPair[writePos].kmer = hashSeqPair[randIdx].kmer;
        hashSeqPair[writePos].pos = hashSeqPair[randIdx].pos;
        hashSeqPair[writePos].seqLen = hashSeqPair[randIdx].seqLen;
        hashSeqPair[writePos].id = hashSeqPair[randIdx].id;
        writePos++;
      }
      prevHashStart = elementIdx;
    }

    if (hashSeqPair[elementIdx].kmer == SIZE_T_MAX) {
      break;
    }
    prevSetSize++;
    prevHash = hashSeqPair[elementIdx].kmer;
    if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
      prevHash = BIT_SET(prevHash, 63);
    }
  }
  hashSeqPair[writePos].kmer = SIZE_T_MAX;
  return writePos;
}

template size_t LinsearchIndexReader::pickCenterKmer<0>(
    mmseqs_output* out, KmerPosition<short> *hashSeqPair, size_t splitKmerCount);
template size_t LinsearchIndexReader::pickCenterKmer<1>(
    mmseqs_output* out, KmerPosition<short> *hashSeqPair, size_t splitKmerCount);

template <int TYPE>
void LinsearchIndexReader::mergeAndWriteIndex(mmseqs_output* out, DBWriter &dbw,
                                              std::vector<std::string> tmpFiles,
                                              int alphSize, int kmerSize) {
  KmerIndex kmerIndex(out, alphSize, kmerSize);

  dbw.writeStart(0);
  out->info("Merge splits ... ");
  const int fileCnt = tmpFiles.size();
  FILE **files = new FILE *[fileCnt];
  KmerPosition<short> **entries = new KmerPosition<short> *[fileCnt];
  size_t *entrySizes = new size_t[fileCnt];
  size_t *offsetPos = new size_t[fileCnt];
  size_t *dataSizes = new size_t[fileCnt];
  // init structures
  for (size_t file = 0; file < tmpFiles.size(); file++) {
    files[file] = FileUtil::openFileOrDie(out, tmpFiles[file].c_str(), "r", true);
    size_t dataSize;
    entries[file] =
        (KmerPosition<short> *)FileUtil::mmapFile(out, files[file], &dataSize);
    dataSizes[file] = dataSize;
    entrySizes[file] = dataSize / sizeof(KmerPosition<short>);
    offsetPos[file] = 0;
  }
  std::priority_queue<FileKmer, std::vector<FileKmer>,
                      CompareRepSequenceAndIdAndDiag>
      queue;
  // read one entry for each file
  for (int file = 0; file < fileCnt; file++) {
    size_t offset = offsetPos[file];
    if (offset < entrySizes[file]) {
      KmerPosition<short> currKmerPosition = entries[file][offset];
      size_t currKmer = currKmerPosition.kmer;
      bool isReverse = false;
      if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
        isReverse = (BIT_CHECK(currKmerPosition.kmer, 63) == false);
        currKmer = BIT_CLEAR(currKmer, 63);
      }
      queue.push(FileKmer(currKmer, currKmerPosition.id, currKmerPosition.pos,
                          currKmerPosition.seqLen, isReverse, file));
    }
  }
  std::string prefResultsOutString;
  prefResultsOutString.reserve(100000000);
  FileKmer res;
  size_t prevKmer = SIZE_T_MAX;
  while (queue.empty() == false) {
    res = queue.top();
    queue.pop();
    {
      size_t offset = offsetPos[res.file];
      if (offset + 1 < entrySizes[res.file]) {
        size_t currKmer = entries[res.file][offset + 1].kmer;
        bool isReverse = false;
        if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
          isReverse =
              (BIT_CHECK(entries[res.file][offset + 1].kmer, 63) == false);
          currKmer = BIT_CLEAR(currKmer, 63);
        }
        queue.push(FileKmer(currKmer, entries[res.file][offset + 1].id,
                            entries[res.file][offset + 1].pos,
                            entries[res.file][offset + 1].seqLen, isReverse,
                            res.file));
        offsetPos[res.file] = offset + 1;
      }
    }
    if (prevKmer != res.kmer) {
      if (kmerIndex.needsFlush(res.kmer) == true) {
        kmerIndex.flush(dbw);
      }
      kmerIndex.addElementSorted(res.kmer, res.id, res.pos, res.seqLen,
                                 res.reverse);
    }
    prevKmer = res.kmer;
  }

  kmerIndex.flush(dbw);
  dbw.writeEnd(PrefilteringIndexReader::ENTRIES, 0);
  dbw.alignToPageSize();
  // clear memory
  for (size_t file = 0; file < tmpFiles.size(); file++) {
    if (fclose(files[file]) != 0) {
      out->failure("Cannot close file {}", tmpFiles[file]);
    }
    FileUtil::munmapData(out, (void *)entries[file], dataSizes[file]);
  }
  delete[] dataSizes;
  delete[] offsetPos;
  delete[] entries;
  delete[] entrySizes;
  delete[] files;

  // write index
  out->info("Write ENTRIESOFFSETS ({})", PrefilteringIndexReader::ENTRIESOFFSETS);
  kmerIndex.setupOffsetTable();
  dbw.writeData((char *)kmerIndex.getOffsets(),
                kmerIndex.getOffsetsSize() * sizeof(size_t),
                PrefilteringIndexReader::ENTRIESOFFSETS, 0);
  dbw.alignToPageSize();

  // write index
  out->info("Write ENTRIESGRIDSIZE ({})", PrefilteringIndexReader::ENTRIESGRIDSIZE);
  uint64_t gridResolution =
      static_cast<uint64_t>(kmerIndex.getGridResolution());
  char *gridResolutionPtr = (char *)&gridResolution;
  dbw.writeData(gridResolutionPtr, 1 * sizeof(uint64_t),
                PrefilteringIndexReader::ENTRIESGRIDSIZE, 0);
  dbw.alignToPageSize();

  // ENTRIESNUM
  out->info("Write ENTRIESNUM ({})", PrefilteringIndexReader::ENTRIESNUM);
  uint64_t entriesNum = kmerIndex.getTableEntriesNum();
  char *entriesNumPtr = (char *)&entriesNum;
  dbw.writeData(entriesNumPtr, 1 * sizeof(uint64_t),
                PrefilteringIndexReader::ENTRIESNUM, 0);
  dbw.alignToPageSize();
}

template void LinsearchIndexReader::mergeAndWriteIndex<0>(
    mmseqs_output* out, DBWriter &dbw, std::vector<std::string> tmpFiles, int alphSize,
    int kmerSize);
template void LinsearchIndexReader::mergeAndWriteIndex<1>(
    mmseqs_output* out, DBWriter &dbw, std::vector<std::string> tmpFiles, int alphSize,
    int kmerSize);

template <int TYPE>
void LinsearchIndexReader::writeIndex(mmseqs_output* out, DBWriter &dbw,
                                      KmerPosition<short> *hashSeqPair,
                                      size_t totalKmers, int alphSize,
                                      int kmerSize) {
  KmerIndex kmerIndex(out, alphSize - 1, kmerSize);
  out->info("Write ENTRIES ({})", PrefilteringIndexReader::ENTRIES
                    );
  // write entries
  dbw.writeStart(0);
  for (size_t pos = 0; pos < totalKmers && hashSeqPair[pos].kmer != SIZE_T_MAX;
       pos++) {
    size_t kmer = hashSeqPair[pos].kmer;
    bool isReverse = false;
    if (TYPE == Parameters::DBTYPE_NUCLEOTIDES) {
      isReverse = (BIT_CHECK(hashSeqPair[pos].kmer, 63) == false);
      kmer = BIT_CLEAR(kmer, 63);
    }
    if (kmerIndex.needsFlush(kmer) == true) {
      kmerIndex.flush(dbw);
    }

    kmerIndex.addElementSorted(kmer, hashSeqPair[pos].id, hashSeqPair[pos].pos,
                               hashSeqPair[pos].seqLen, isReverse);
  }
  kmerIndex.flush(dbw);
  dbw.writeEnd(PrefilteringIndexReader::ENTRIES, 0);
  dbw.alignToPageSize();

  // write index
  out->info("Write ENTRIESOFFSETS ({})", PrefilteringIndexReader::ENTRIESOFFSETS);
  kmerIndex.setupOffsetTable();
  dbw.writeData((char *)kmerIndex.getOffsets(),
                kmerIndex.getOffsetsSize() * sizeof(size_t),
                PrefilteringIndexReader::ENTRIESOFFSETS, 0);
  dbw.alignToPageSize();

  // write index
  out->info("Write ENTRIESGRIDSIZE ({})", PrefilteringIndexReader::ENTRIESGRIDSIZE);
  uint64_t gridResolution =
      static_cast<uint64_t>(kmerIndex.getGridResolution());
  char *gridResolutionPtr = (char *)&gridResolution;
  dbw.writeData(gridResolutionPtr, 1 * sizeof(uint64_t),
                PrefilteringIndexReader::ENTRIESGRIDSIZE, 0);
  dbw.alignToPageSize();

  // ENTRIESNUM
  out->info("Write ENTRIESNUM ({})", PrefilteringIndexReader::ENTRIESNUM);
  uint64_t entriesNum = kmerIndex.getTableEntriesNum();
  char *entriesNumPtr = (char *)&entriesNum;
  dbw.writeData(entriesNumPtr, 1 * sizeof(uint64_t),
                PrefilteringIndexReader::ENTRIESNUM, 0);
  dbw.alignToPageSize();
}

template void LinsearchIndexReader::writeIndex<0>(
    mmseqs_output* out, DBWriter &dbw, KmerPosition<short> *hashSeqPair, size_t totalKmers,
    int alphSize, int kmerSize);
template void LinsearchIndexReader::writeIndex<1>(
    mmseqs_output* out, DBWriter &dbw, KmerPosition<short> *hashSeqPair, size_t totalKmers,
    int alphSize, int kmerSize);

std::string LinsearchIndexReader::indexName(mmseqs_output* out, std::string baseName) {
  std::string result(baseName);
  result.append(".").append("linidx");
  return result;
}

bool LinsearchIndexReader::checkIfIndexFile(mmseqs_output* out, DBReader<unsigned int> *pReader) {
  char *version = pReader->getDataByDBKey(PrefilteringIndexReader::VERSION, 0);
  if (version == NULL) {
    return false;
  }
  return (strncmp(version, PrefilteringIndexReader::CURRENT_VERSION,
                  strlen(PrefilteringIndexReader::CURRENT_VERSION)) == 0)
             ? true
             : false;
}

void LinsearchIndexReader::writeKmerIndexToDisk(mmseqs_output* out, std::string fileName,
                                                KmerPosition<short> *kmers,
                                                size_t kmerCnt) {
  FILE *filePtr = fopen(fileName.c_str(), "wb");
  if (filePtr == NULL) {
    perror(fileName.c_str());
    out->failure("File cannot be opened: {}", fileName);
  }
  fwrite(kmers, sizeof(KmerPosition<unsigned short>), kmerCnt, filePtr);
  if (fclose(filePtr) != 0) {
    out->failure("Cannot close file {}", fileName);
  }
}

std::string LinsearchIndexReader::findIncompatibleParameter(
    mmseqs_output* out, DBReader<unsigned int> &index, Parameters &par, int dbtype) {
  PrefilteringIndexData meta = PrefilteringIndexReader::getMetadata(&index);
  if (meta.maxSeqLength != static_cast<int>(par.maxSeqLen)) return "maxSeqLen";
  if (meta.seqType != dbtype) return "seqType";
  if (Parameters::isEqualDbtype(dbtype, Parameters::DBTYPE_NUCLEOTIDES) ==
          false &&
      meta.alphabetSize != par.alphabetSize.aminoacids)
    return "alphabetSize";
  if (meta.kmerSize != par.kmerSize) return "kmerSize";
  if (meta.mask != (par.maskMode > 0)) return "maskMode";
  if (meta.spacedKmer != par.spacedKmer) return "spacedKmer";
  if (BaseMatrix::unserializeName(par.seedScoringMatrixFile.aminoacids) !=
          PrefilteringIndexReader::getSubstitutionMatrixName(&index) &&
      BaseMatrix::unserializeName(par.seedScoringMatrixFile.nucleotides) !=
          PrefilteringIndexReader::getSubstitutionMatrixName(&index))
    return "seedScoringMatrixFile";
  if (par.spacedKmerPattern !=
      PrefilteringIndexReader::getSpacedPattern(&index))
    return "spacedKmerPattern";
  return "";
}

std::string LinsearchIndexReader::searchForIndex(mmseqs_output* out, const std::string &dbName) {
  std::string outIndexName = dbName + ".linidx";
  if (FileUtil::fileExists(out, (outIndexName + ".dbtype").c_str()) == true) {
    return outIndexName;
  }
  return "";
}

#undef SIZE_T_MAX
