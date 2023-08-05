#include <mmseqs/commons/commandCaller.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/taxonomy/ncbiTaxonomy.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#include "createtaxdb.sh.h"

int createtaxdb(mmseqs_output* out, Parameters& par) {
  //    Parameters& par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  std::string tmp = par.filenames.back();
  if (FileUtil::directoryExists(out, tmp.c_str()) == false) {
    out->info("Tmp {} folder does not exist or is not a directory.", tmp
                      );
    if (FileUtil::makeDir(out, tmp.c_str()) == false) {
      out->failure("Can not create tmp folder {}.", tmp);
    } else {
      out->info("Created dir {}", tmp);
    }
  }
  CommandCaller cmd(out);

  cmd.addVariable("TMP_PATH", tmp.c_str());
  if (par.taxMappingFile.empty()) {
    cmd.addVariable("DOWNLOAD_MAPPING", "1");
  } else {
    cmd.addVariable("DOWNLOAD_MAPPING", "0");
    cmd.addVariable("MAPPINGFILE", par.taxMappingFile.c_str());
  }
  cmd.addVariable("MAPPINGMODE", SSTR(par.taxMappingMode).c_str());
  cmd.addVariable("DBMODE", SSTR(par.taxDbMode).c_str());
  if (par.ncbiTaxDump.empty()) {
    cmd.addVariable("DOWNLOAD_NCBITAXDUMP", "1");
  } else {
    cmd.addVariable("DOWNLOAD_NCBITAXDUMP", "0");
    cmd.addVariable("NCBITAXINFO", par.ncbiTaxDump.c_str());
  }
  cmd.addVariable("ARIA_NUM_CONN", SSTR(std::min(16, par.threads)).c_str());
  cmd.addVariable("VERBOSITY_PAR",
                  par.createParameterString(out, par.onlyverbosity).c_str());
  FileUtil::writeFile(out, tmp + "/createindex.sh", createtaxdb_sh,
                      createtaxdb_sh_len);
  std::string program(tmp + "/createindex.sh");
  cmd.execProgram(program.c_str(), par.filenames);

  return EXIT_SUCCESS;
}
