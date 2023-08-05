#include <mmseqs/commons/commandCaller.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#include "multihitsearch.sh.h"

void setMultiHitSearchWorkflowDefaults(Parameters *p) {
  p->sensitivity = 5.7;
  // TODO: Check query cov maybe?
  // p->covThr = 0.7;
  p->evalThr = 100;

  // TODO: Needs to be more than the count of target sets (10x?)
  p->maxSequences = 1500;

  // TODO: Why??
  // p->scoreBias = 0.3;

  p->simpleBestHit = true;
  // TODO: add a minimum alignment length cutoff, 4 residue alignments dont seem
  // useful

  // Set alignment mode
  p->alignmentMode = Parameters::ALIGNMENT_MODE_SCORE_COV;
}

int multihitsearch(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    setMultiHitSearchWorkflowDefaults(&par);
  //
  //    par.PARAM_MAX_REJECTED.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_DB_OUTPUT.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_OVERLAP.addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    for (size_t i = 0; i < par.extractorfs.size(); i++){
  //        par.extractorfs[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    for (size_t i = 0; i < par.translatenucs.size(); i++){
  //        par.translatenucs[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    for (size_t i = 0; i < par.splitsequence.size(); i++) {
  //        par.splitsequence[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    for (size_t i = 0; i < par.result2profile.size(); i++){
  //        par.result2profile[i]->addCategory(MMseqsParameter::COMMAND_EXPERT);
  //    }
  //    par.PARAM_COMPRESSED.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_THREADS.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //    par.PARAM_V.removeCategory(MMseqsParameter::COMMAND_EXPERT);
  //
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  if (FileUtil::directoryExists(out, par.db4.c_str()) == false) {
    out->info("Tmp {} folder does not exist or is not a directory.", par.db4
                      );
    if (FileUtil::makeDir(out, par.db4.c_str()) == false) {
      out->failure("Can not create tmp folder {}", par.db4 );
    } else {
      out->info("Created dir {}", par.db4);
    }
  }
  size_t hash =
      par.hashParameter(out, par.databases_types, par.filenames, par.multihitsearch);
  std::string tmpDir = par.db4 + "/" + SSTR(hash);
  if (FileUtil::directoryExists(out, tmpDir.c_str()) == false) {
    if (FileUtil::makeDir(out, tmpDir.c_str()) == false) {
      out->failure("Can not create sub tmp folder {}", tmpDir);
    }
  }
  par.filenames.pop_back();
  par.filenames.push_back(tmpDir);
  FileUtil::symlinkAlias(out, tmpDir, "latest");

  CommandCaller cmd(out);
  if (par.removeTmpFiles) {
    cmd.addVariable("REMOVE_TMP", "TRUE");
  }
  cmd.addVariable("SEARCH_PAR",
                  par.createParameterString(out, par.searchworkflow).c_str());
  cmd.addVariable("BESTHITBYSET_PAR",
                  par.createParameterString(out, par.besthitbyset).c_str());
  cmd.addVariable("THREADS_PAR",
                  par.createParameterString(out, par.onlythreads).c_str());
  cmd.addVariable("VERBOSITY",
                  par.createParameterString(out, par.onlyverbosity).c_str());

  FileUtil::writeFile(out, tmpDir + "/multihitsearch.sh", multihitsearch_sh,
                      multihitsearch_sh_len);
  std::string program(tmpDir + "/multihitsearch.sh");
  cmd.execProgram(program.c_str(), par.filenames);

  return EXIT_SUCCESS;
}
