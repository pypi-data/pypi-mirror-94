#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

int mergeresultsbyset(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, true, 0);

  DBReader<unsigned int> setReader(
      out, par.db1.c_str(), par.db1Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  setReader.open(DBReader<unsigned int>::LINEAR_ACCCESS);

  DBReader<unsigned int> resultReader(
      out, par.db2.c_str(), par.db2Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  resultReader.open(DBReader<unsigned int>::NOSORT);

  DBWriter dbw(out, par.db3.c_str(), par.db3Index.c_str(), par.threads,
               par.compressed, resultReader.getDbtype());
  dbw.open();
#pragma omp parallel
  {
    int thread_idx = 0;
#ifdef OPENMP
    thread_idx = omp_get_thread_num();
#endif
    std::string buffer;
    buffer.reserve(10 * 1024);
    char dbKey[255];
#pragma omp for schedule(static)
    for (size_t i = 0; i < setReader.getSize(); ++i) {
      char *data = setReader.getData(i, thread_idx);
      // go through the results in the cluster and add them to one entry
      while (*data != '\0') {
        Util::parseKey(data, dbKey);
        unsigned int key = Util::fast_atoi<unsigned int>(dbKey);
        size_t id = resultReader.getId(key);
        if (id == UINT_MAX) {
          out->failure("Invalid key {} in entry {}", key, data);
        }
        buffer.append(resultReader.getData(id, thread_idx));
        data = Util::skipLine(data);
      }
      dbw.writeData(buffer.c_str(), buffer.length(), setReader.getDbKey(i),
                    thread_idx);
      buffer.clear();
    }
  }
  dbw.close();
  resultReader.close();
  setReader.close();

  return EXIT_SUCCESS;
}
