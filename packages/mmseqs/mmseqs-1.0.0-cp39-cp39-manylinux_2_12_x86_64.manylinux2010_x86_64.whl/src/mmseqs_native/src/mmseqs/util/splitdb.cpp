#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

int splitdb(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  if (par.split < 1) {
    out->failure("Cannot split databases into 0 or negative chunks.");
  }

  DBReader<unsigned int> dbr(
      out, par.db1.c_str(), par.db1Index.c_str(), 1,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  dbr.open(DBReader<unsigned int>::NOSORT);

  if ((size_t)par.split > dbr.getSize()) {
    out->failure("Cannot split databases into more chunks than database contains");
  }

  for (int split = 0; split < par.split; split++) {
    std::string outDb = par.db2 + "_" + SSTR(split) + "_" + SSTR(par.split);
    DBWriter writer(out, outDb.c_str(), std::string(outDb + ".index").c_str(), 1,
                    par.compressed, dbr.getDbtype());
    writer.open();

    size_t startIndex = 0;
    size_t domainSize = 0;
    if (par.splitAA) {
      dbr.decomposeDomainByAminoAcid(split, par.split, &startIndex,
                                     &domainSize);
    } else {
      Util::decomposeDomain(out, dbr.getSize(), split, par.split, &startIndex,
                            &domainSize);
    }

    for (size_t i = startIndex; i < (startIndex + domainSize); i++) {
      unsigned int outerKey = dbr.getDbKey(i);
      char *data = dbr.getData(i, 0);
      writer.writeData(data, dbr.getEntryLen(i) - 1, outerKey);
    }
    writer.close();
    DBReader<unsigned int>::softlinkDb(out, par.db1, outDb,
                                       DBFiles::SEQUENCE_ANCILLARY);
  }

  dbr.close();
  return EXIT_SUCCESS;
}
