#include <cassert>

#include <mmseqs/commons/commandCaller.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

namespace linclust_utils {
#include "easycluster.sh.h"
}

void setEasyLinclustDefaults(Parameters *p) {
  p->spacedKmer = false;
  p->removeTmpFiles = true;
  p->covThr = 0.8;
  p->evalThr = 0.001;
  p->createdbMode = Parameters::SEQUENCE_SPLIT_MODE_SOFT;
  p->writeLookup = false;
  // p->alignmentMode = Parameters::ALIGNMENT_MODE_SCORE_COV_SEQID;
  p->orfStartMode = 1;
  p->orfMinLength = 10;
  p->orfMaxLength = 32734;
  p->evalProfile = 0.1;
}
void setEasyLinclustMustPassAlong(Parameters *p) {
  p->PARAM_SPACED_KMER_MODE.wasSet = true;
  p->PARAM_REMOVE_TMP_FILES.wasSet = true;
  p->PARAM_C.wasSet = true;
  p->PARAM_E.wasSet = true;
  // p->PARAM_ALIGNMENT_MODE.wasSet = true;
  p->PARAM_ORF_START_MODE.wasSet = true;
  p->PARAM_ORF_MIN_LENGTH.wasSet = true;
  p->PARAM_ORF_MAX_LENGTH.wasSet = true;
  p->PARAM_E_PROFILE.wasSet = true;
}

int easylinclust(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.PARAM_ADD_BACKTRACE.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_ALT_ALIGNMENT.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_RESCORE_MODE.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_ZDROP.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_MAX_REJECTED.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_MAX_ACCEPT.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.overrideParameterDescription(par.PARAM_S, "Sensitivity will be
  //    automatically determined but can be adjusted", NULL,
  //    par.PARAM_S.category | MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_INCLUDE_ONLY_EXTENDABLE.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    for (size_t i = 0; i < par.createdb.size(); i++){
  //        par.createdb[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    par.PARAM_COMPRESSED.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_THREADS.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_V.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //
  //    setEasyLinclustDefaults(&par);
  //    par.parseParameters(argc, argv, command, true,
  //    Parameters::PARSE_VARIADIC, 0);
  setEasyLinclustMustPassAlong(&par);

  std::string tmpDir = par.filenames.back();
  // TODO: Fix
  std::string hash = "abc";  // STR(par.hashParameter(par.databases_types,
                             // par.filenames, *command.params));
  if (par.reuseLatest) {
    hash = FileUtil::getHashFromSymLink(out, tmpDir + "/latest");
  }
  tmpDir = FileUtil::createTemporaryDirectory(out, par.baseTmpPath, tmpDir, hash);
  par.filenames.pop_back();

  CommandCaller cmd(out);
  cmd.addVariable("TMP_PATH", tmpDir.c_str());
  cmd.addVariable("RESULTS", par.filenames.back().c_str());
  par.filenames.pop_back();
  cmd.addVariable("REMOVE_TMP", par.removeTmpFiles ? "TRUE" : NULL);

  cmd.addVariable("RUNNER", par.runner.c_str());
  cmd.addVariable("CREATEDB_PAR",
                  par.createParameterString(out, par.createdb).c_str());
  cmd.addVariable(
      "CLUSTER_PAR",
      par.createParameterString(out, par.linclustworkflow, true).c_str());
  cmd.addVariable("CLUSTER_MODULE", "linclust");
  cmd.addVariable("RESULT2REPSEQ_PAR",
                  par.createParameterString(out, par.result2repseq).c_str());
  cmd.addVariable("THREADS_PAR",
                  par.createParameterString(out, par.onlythreads).c_str());
  cmd.addVariable("VERBOSITY_PAR",
                  par.createParameterString(out, par.onlyverbosity).c_str());

  std::string program = tmpDir + "/easycluster.sh";
  FileUtil::writeFile(out, program, linclust_utils::easycluster_sh,
                      linclust_utils::easycluster_sh_len);
  cmd.execProgram(program.c_str(), par.filenames);

  // Should never get here
  assert(false);
  return 0;
}
