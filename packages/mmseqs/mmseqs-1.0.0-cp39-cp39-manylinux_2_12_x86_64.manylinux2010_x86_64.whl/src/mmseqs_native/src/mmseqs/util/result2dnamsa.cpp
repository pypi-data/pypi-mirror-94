// Computes MSAs from clustering or alignment result

#include <mmseqs/alignment/matcher.h>
#include <mmseqs/commons/orf.h>
#include <sstream>
#include <string>
#include <vector>

#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

int result2dnamsa(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  DBReader<unsigned int> qDbr(
      out, par.db1.c_str(), par.db1Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  qDbr.open(DBReader<unsigned int>::NOSORT);

  DBReader<unsigned int> queryHeaderReader(
      out, par.hdr1.c_str(), par.hdr1Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  // NOSORT because the index should be in the same order as resultReader
  queryHeaderReader.open(DBReader<unsigned int>::NOSORT);

  DBReader<unsigned int> *tDbr = &qDbr;
  DBReader<unsigned int> *tempateHeaderReader = &queryHeaderReader;

  const bool sameDatabase = (par.db1.compare(par.db2) == 0) ? true : false;
  if (!sameDatabase) {
    tDbr = new DBReader<unsigned int>(
        out, par.db2.c_str(), par.db2Index.c_str(), par.threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    tDbr->open(DBReader<unsigned int>::NOSORT);

    tempateHeaderReader = new DBReader<unsigned int>(
        out, par.hdr2.c_str(), par.hdr2Index.c_str(), par.threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    tempateHeaderReader->open(DBReader<unsigned int>::NOSORT);
  }

  DBReader<unsigned int> resultReader(
      out, par.db3.c_str(), par.db3Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  resultReader.open(DBReader<unsigned int>::LINEAR_ACCCESS);

  DBWriter resultWriter(out, par.db4.c_str(), par.db4Index.c_str(), par.threads,
                        par.compressed, Parameters::DBTYPE_MSA_DB);
  resultWriter.open();

  out->info("Query database size: {} type: {}. Target database size: {} type: {}", qDbr.getSize(), qDbr.getDbTypeName(), tDbr->getSize(), tDbr->getDbTypeName());
  Log::Progress progress(resultReader.getSize());

#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = (unsigned int)omp_get_thread_num();
#endif
    std::vector<Matcher::result_t> alnResults;
    std::string out_str;

#pragma omp for schedule(dynamic, 10)
    for (size_t id = 0; id < resultReader.getSize(); id++) {
      progress.updateProgress();
      alnResults.clear();
      // Get the sequence from the queryDB
      unsigned int queryKey = resultReader.getDbKey(id);
      size_t queryId = qDbr.getId(queryKey);
      resultWriter.writeStart(thread_idx);

      if (par.skipQuery == false) {
        char *centerSequenceHeader =
            queryHeaderReader.getData(queryId, thread_idx);
        resultWriter.writeAdd(">", 1, thread_idx);
        resultWriter.writeAdd(centerSequenceHeader,
                              queryHeaderReader.getSeqLen(queryId) + 1,
                              thread_idx);
        char *seq = qDbr.getData(queryId, 0);
        resultWriter.writeAdd(seq, qDbr.getSeqLen(queryId) + 1, thread_idx);
      }
      Matcher::readAlignmentResults(
          out, alnResults, resultReader.getData(id, thread_idx), false);
      for (size_t i = 0; i < alnResults.size(); i++) {
        Matcher::result_t res = alnResults[i];
        bool queryIsReversed = (res.qStartPos > res.qEndPos);
        const size_t targetId = tDbr->getId(res.dbKey);
        out_str.clear();
        char *templateHeader =
            tempateHeaderReader->getData(targetId, thread_idx);
        resultWriter.writeAdd(">", 1, thread_idx);
        resultWriter.writeAdd(templateHeader,
                              tempateHeaderReader->getSeqLen(targetId) + 1,
                              thread_idx);
        char *targetSeq = tDbr->getData(targetId, thread_idx);
        unsigned int seqPos = 0;
        bool targetIsReversed = (res.dbStartPos > res.dbEndPos);

        bool isReverseStrand = false;
        if (queryIsReversed == true && targetIsReversed == true) {
          std::swap(res.dbStartPos, res.dbEndPos);
          std::reverse(res.backtrace.begin(), res.backtrace.end());
        } else if (queryIsReversed == true && targetIsReversed == false) {
          isReverseStrand = true;
          std::swap(res.dbStartPos, res.dbEndPos);
          std::reverse(res.backtrace.begin(), res.backtrace.end());
        } else if (queryIsReversed == false && targetIsReversed == true) {
          isReverseStrand = true;
        }

        int qStartPos = std::min(res.qStartPos, res.qEndPos);
        for (int pos = 0; pos < qStartPos; ++pos) {
          out_str.push_back('-');
        }
        for (uint32_t pos = 0; pos < res.backtrace.size(); ++pos) {
          char seqChar =
              (isReverseStrand == true)
                  ? Orf::complement(targetSeq[res.dbStartPos - seqPos])
                  : targetSeq[res.dbStartPos + seqPos];
          switch (res.backtrace[pos]) {
            case 'M':
              out_str.push_back(seqChar);
              seqPos++;
              break;
            case 'I':
              out_str.push_back('-');
              break;
            case 'D':
              seqPos++;
              break;
          }
        }
        int qEndPos = std::max(res.qStartPos, res.qEndPos);
        for (unsigned int pos = qEndPos + 1; pos < res.qLen; ++pos) {
          out_str.push_back('-');
        }
        out_str.push_back('\n');
        resultWriter.writeAdd(out_str.c_str(), out_str.size(), thread_idx);
      }
      resultWriter.writeEnd(queryKey, thread_idx);
    }
  }

  // cleanup
  resultWriter.close(true);
  resultReader.close();
  queryHeaderReader.close();
  qDbr.close();

  if (!sameDatabase) {
    tempateHeaderReader->close();
    delete tempateHeaderReader;
    tDbr->close();
    delete tDbr;
  }

  return EXIT_SUCCESS;
}
