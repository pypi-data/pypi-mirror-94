#include <mmseqs/commons/commandCaller.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include "easytaxonomy.sh.h"
#include <mmseqs/output.h>

void setEasyTaxonomyDefaults(Parameters *p) {
  p->removeTmpFiles = true;
  p->createdbMode = Parameters::SEQUENCE_SPLIT_MODE_SOFT;
  p->writeLookup = false;
}
void setEasyTaxonomyMustPassAlong(Parameters *p) {
  p->PARAM_REMOVE_TMP_FILES.wasSet = true;
  p->PARAM_CREATEDB_MODE.wasSet = true;
  p->PARAM_WRITE_LOOKUP.wasSet = true;
}

int easytaxonomy(mmseqs_output *out, Parameters &par) {
  //    Parameters& par = Parameters::getInstance();
  //
  //    for (size_t i = 0; i < par.createdb.size(); i++){
  //        par.createdb[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    for (size_t i = 0; i < par.searchworkflow.size(); i++){
  //        par.searchworkflow[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    for (size_t i = 0; i < par.convertalignments.size(); i++){
  //        par.convertalignments[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    for (size_t i = 0; i < par.createtsv.size(); i++){
  //        par.createtsv[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    par.PARAM_S.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_E.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_COMPRESSED.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_THREADS.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_V.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //
  //    setEasyTaxonomyDefaults(&par);
  //    par.parseParameters(argc, argv, command, true,
  //    Parameters::PARSE_VARIADIC, 0);
  setEasyTaxonomyMustPassAlong(&par);

  std::string tmpDir = par.filenames.back();
  // TODO: Fix
  std::string hash = "abc";  // SSTR(par.hashParameter(par.databases_types,
                             // par.filenames, *command.params));
  if (par.reuseLatest) {
    hash = FileUtil::getHashFromSymLink(out, tmpDir + "/latest");
  }
  tmpDir = FileUtil::createTemporaryDirectory(out, par.baseTmpPath, tmpDir, hash);
  par.filenames.pop_back();

  CommandCaller cmd(out);
  cmd.addVariable("RESULTS", par.filenames.back().c_str());
  par.filenames.pop_back();
  cmd.addVariable("TARGET", par.filenames.back().c_str());
  par.filenames.pop_back();
  cmd.addVariable("TMP_PATH", tmpDir.c_str());
  cmd.addVariable("REMOVE_TMP", par.removeTmpFiles ? "TRUE" : NULL);
  cmd.addVariable("RUNNER", par.runner.c_str());
  cmd.addVariable("VERBOSITY",
                  par.createParameterString(out, par.onlyverbosity).c_str());

  par.taxonomyOutputMode = Parameters::TAXONOMY_OUTPUT_BOTH;
  par.PARAM_TAX_OUTPUT_MODE.wasSet = true;
  cmd.addVariable("TAXONOMY_PAR",
                  par.createParameterString(out, par.taxonomy, true).c_str());
  cmd.addVariable("CREATEDB_QUERY_PAR",
                  par.createParameterString(out, par.createdb).c_str());
  cmd.addVariable("LCA_PAR", par.createParameterString(out, par.lca).c_str());
  cmd.addVariable("CONVERT_PAR",
                  par.createParameterString(out, par.convertalignments).c_str());
  cmd.addVariable("TAXONOMYREPORT_PAR",
                  par.createParameterString(out, par.taxonomyreport).c_str());
  cmd.addVariable("CREATETSV_PAR",
                  par.createParameterString(out, par.createtsv).c_str());
  par.evalThr = FLT_MAX;
  cmd.addVariable("SWAPRESULT_PAR",
                  par.createParameterString(out, par.swapresult).c_str());
  par.pickIdFrom = 1;
  cmd.addVariable("ADDTAXONOMY_PAR",
                  par.createParameterString(out, par.addtaxonomy).c_str());
  cmd.addVariable("THREADS_COMP_PAR",
                  par.createParameterString(out, par.threadsandcompression).c_str());
  FileUtil::writeFile(out, tmpDir + "/easy-taxonomy.sh", easytaxonomy_sh,
                      easytaxonomy_sh_len);
  std::string program(tmpDir + "/easy-taxonomy.sh");
  cmd.execProgram(program.c_str(), par.filenames);

  return EXIT_SUCCESS;
}
