#ifndef RESULT2PROFILE_H
#define RESULT2PROFILE_H

#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/output.h>

#include <unordered_map>

class StatsComputer {
 public:
  StatsComputer(mmseqs_output* output, const Parameters &par);
  ~StatsComputer();

  int run();

 private:
  mmseqs_output* out;
  int stat;

  std::string queryDb;
  std::string queryDbIndex;

  std::string targetDb;
  std::string targetDbIndex;

  const bool tsvOut;

  DBReader<unsigned int> *resultReader;
  DBWriter *statWriter;

  int threads;

  template <typename T>
  struct PerSequence {
    typedef T (*type)(const char *);
  };

  template <typename T>
  int sequenceWise(mmseqs_output* out, typename PerSequence<T>::type call,
                   bool onlyResultDb = false);

  int countNumberOfLines();
  int meanValue();
  int sumValue();
};

#endif
