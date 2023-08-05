#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/mMseqsMPI.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/prefiltering/prefiltering.h>
#include <mmseqs/commons/timer.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

int prefilter(mmseqs_output* out, Parameters& par) {
  //    MMseqsMPI::init(argc, argv);
  //
  //    Parameters& par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0,
  //    MMseqsParameter::COMMAND_PREFILTER);

  Timer timer;
  int queryDbType = FileUtil::parseDbType(out, par.db1.c_str());
  int targetDbType = FileUtil::parseDbType(out, par.db2.c_str());
  if (Parameters::isEqualDbtype(targetDbType, Parameters::DBTYPE_INDEX_DB) ==
      true) {
    DBReader<unsigned int> dbr(
        out,
        par.db2.c_str(), par.db2Index.c_str(), par.threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    dbr.open(DBReader<unsigned int>::NOSORT);
    PrefilteringIndexData data = PrefilteringIndexReader::getMetadata(&dbr);
    targetDbType = data.seqType;
    dbr.close();
  }
  if (queryDbType == -1 || targetDbType == -1) {
    out->error("Please recreate your database or add a .dbtype file to your sequence/profile database.");
    return EXIT_FAILURE;
  }
  if (Parameters::isEqualDbtype(queryDbType, Parameters::DBTYPE_HMM_PROFILE) &&
      Parameters::isEqualDbtype(targetDbType, Parameters::DBTYPE_HMM_PROFILE)) {
    out->error("Only the query OR the target database can be a profile database.");
    return EXIT_FAILURE;
  }

  if (Parameters::isEqualDbtype(queryDbType, Parameters::DBTYPE_AMINO_ACIDS) &&
      Parameters::isEqualDbtype(targetDbType, Parameters::DBTYPE_NUCLEOTIDES)) {
    out->error("The prefilter can not search amino acids against nucleotides. Something might got wrong while createdb or createindex");
    return EXIT_FAILURE;
  }
  if (Parameters::isEqualDbtype(queryDbType, Parameters::DBTYPE_NUCLEOTIDES) &&
      Parameters::isEqualDbtype(targetDbType, Parameters::DBTYPE_AMINO_ACIDS)) {
    out->error("The prefilter can not search nucleotides against amino acids. Something might got wrong while createdb or createindex.");
    return EXIT_FAILURE;
  }
  if (Parameters::isEqualDbtype(queryDbType, Parameters::DBTYPE_HMM_PROFILE) ==
          false &&
      Parameters::isEqualDbtype(targetDbType,
                                Parameters::DBTYPE_PROFILE_STATE_SEQ)) {
    out->error("The query has to be a profile when using a target profile state database.");
    return EXIT_FAILURE;
  } else if (Parameters::isEqualDbtype(queryDbType,
                                       Parameters::DBTYPE_HMM_PROFILE) &&
             Parameters::isEqualDbtype(targetDbType,
                                       Parameters::DBTYPE_PROFILE_STATE_SEQ)) {
    queryDbType = Parameters::DBTYPE_PROFILE_STATE_PROFILE;
  }

  Prefiltering pref(out, par.db1, par.db1Index, par.db2, par.db2Index,
                    queryDbType, targetDbType, par);

#ifdef HAVE_MPI
  int runRandomId = 0;
  if (par.localTmp != "") {
    std::srand(
        std::time(nullptr));  // use current time as seed for random generator
    runRandomId = std::rand();
    runRandomId =
        runRandomId / 2;  // to avoid the unlikely case of overflowing later
  }
  pref.runMpiSplits(out, par.db3, par.db3Index, par.localTmp, runRandomId);
#else
  pref.runAllSplits(out, par.db3, par.db3Index);
#endif

  return EXIT_SUCCESS;
}
