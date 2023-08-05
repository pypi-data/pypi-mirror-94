#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

int result2repseq(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  DBReader<unsigned int> seqReader(
      out, par.db1.c_str(), par.db1Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  seqReader.open(DBReader<unsigned int>::NOSORT);
  if (par.preloadMode != Parameters::PRELOAD_MODE_MMAP) {
    seqReader.readMmapedDataInMemory();
  }

  DBReader<unsigned int> resultReader(
      out, par.db2.c_str(), par.db2Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  resultReader.open(DBReader<unsigned int>::LINEAR_ACCCESS);

  DBWriter resultWriter(out, par.db3.c_str(), par.db3Index.c_str(), par.threads,
                        par.compressed, seqReader.getDbtype());
  resultWriter.open();

  Log::Progress progress(resultReader.getSize());
#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = (unsigned int)omp_get_thread_num();
#endif

    char dbKey[255];
#pragma omp for schedule(dynamic, 100)
    for (size_t id = 0; id < resultReader.getSize(); ++id) {
      progress.updateProgress();

      char *results = resultReader.getData(id, thread_idx);
      if (*results == '\0') {
        continue;
      }

      Util::parseKey(results, dbKey);
      const unsigned int key = (unsigned int)strtoul(dbKey, NULL, 10);
      const size_t edgeId = seqReader.getId(key);
      resultWriter.writeData(seqReader.getData(edgeId, thread_idx),
                             seqReader.getEntryLen(edgeId) - 1,
                             resultReader.getDbKey(id), thread_idx);
    }
  }
  resultWriter.close(true);
  resultReader.close();
  seqReader.close();
  DBReader<unsigned int>::softlinkDb(out, par.db1, par.db3,
                                     DBFiles::SEQUENCE_ANCILLARY);

  return EXIT_SUCCESS;
}
