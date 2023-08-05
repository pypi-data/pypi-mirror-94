#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/mathUtil.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/sequence.h>
#include <mmseqs/commons/substitutionMatrix.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include "omp.h"
#endif

void parseHMM(mmseqs_output* out, char *data, std::string *sequence, std::string *header,
              char *profileBuffer, size_t *size, unsigned int id,
              BaseMatrix *subMat) {
  // find name tag
  while (data[0] != 'N' || data[1] != 'A' || data[2] != 'M' || data[3] != 'E') {
    data = Util::skipLine(data);
  }

  // parse NAME entry
  const char *startData = data;
  data = Util::skipLine(data);
  const char *endData = data;
  header->append(startData + 6, endData - (startData + 6));

  // >Consensus
  while (strncmp(">Consensus", data, 10) != 0) {
    data = Util::skipLine(data);
  }
  // skip over Cons. header
  data = Util::skipLine(data);
  // find first line after >Consensus that starts with a >
  while (data[0] != '>') {
    data = Util::skipLine(data);
  }
  data = Util::skipLine(data);
  char *seqStartPos = data;
  // copy sequence
  while (data[0] != '>' && data[0] != '#') {
    data = Util::skipLine(data);
  }
  char *seqEndPos = data;
  size_t len = (seqEndPos - seqStartPos);
  for (size_t i = 0; i < len; i++) {
    if (seqStartPos[i] != '\n') sequence->push_back(seqStartPos[i]);
  }
  sequence->push_back('\n');

  // find beginning of profile information
  while (data[0] != '#') {
    data = Util::skipLine(data);
  }

  // go to readin position
  for (int i = 0; i < 5; i++) {
    data = Util::skipLine(data);
  }

  // ammino acids are ordered in HMM
  const char *words[22];
  float probs[20];
  int seq_pos = 0;
  size_t curr_pos = 0;
  while (data[0] != '/' && data[1] != '/') {
    Util::getWordsOfLine(data, words, 22);
    for (size_t aa_num = 0; aa_num < 20; aa_num++) {
      // entry: 0.0 probability
      if (words[aa_num + 2][0] == '*') {
        probs[aa_num] = 0.0;
      } else if (words[aa_num + 2][0] == '0') {
        // 0 entry: 1.0 probability
        // integer number entry: 0.0 < probability < 1.0
        probs[aa_num] = 1.0;
      } else {
        int entry = Util::fast_atoi<int>(words[aa_num + 2]);
        // back scaling from hhm
        const float p = MathUtil::fpow2(-(entry / 1000.0f));
        probs[aa_num] = p;
      }
      // shifted score by -128 to avoid \0
      profileBuffer[curr_pos] = Sequence::scoreMask(probs[aa_num]);

      if (profileBuffer[curr_pos] == 0) {
        out->failure("PSSM score of 0 is too large at id: {}.hhm, pos: {}, socre: {}", id, curr_pos, (char)(profileBuffer[curr_pos] ^ 0x80));
      }
      curr_pos++;
    }

    float maxw = 0.0;
    int maxa = 21;
    for (size_t aa = 0; aa < Sequence::PROFILE_AA_SIZE; ++aa) {
      float prob = probs[aa];
      const float backProb = subMat->getBackgroundProb(aa);
      if (prob - backProb > maxw) {
        maxw = prob - backProb;
        maxa = aa;
      }
    }
    // write query, consensus and neff
    profileBuffer[curr_pos] =
        subMat->aa2num[static_cast<int>(sequence->at(seq_pos))];
    curr_pos++;
    profileBuffer[curr_pos] = maxa;
    curr_pos++;
    Util::getWordsOfLine(data, words, 22);
    int entry = Util::fast_atoi<int>(words[7]);  // NEFF value
    const float neff = static_cast<float>(entry) / 1000.0f;
    profileBuffer[curr_pos] = MathUtil::convertNeffToChar(neff);
    curr_pos++;
    seq_pos++;
    // go to next entry start and skip transitions
    for (int i = 0; i < 3; i++) data = Util::skipLine(data);
  }

  // return size of buffer
  *size = curr_pos;
}

int convertprofiledb(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  std::string data = par.db1;
  std::string index = par.db1Index;
  if (FileUtil::fileExists(out, (par.db1 + ".ffdata").c_str()) &&
      FileUtil::fileExists(out, (par.db1 + ".ffindex").c_str())) {
    data = par.db1 + ".ffdata";
    index = par.db1 + ".ffindex";
  }
  DBReader<std::string> reader(out,
      data.c_str(), index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  reader.open(DBReader<std::string>::NOSORT);

  DBWriter profileWriter(out, par.db2.c_str(), par.db2Index.c_str(), par.threads,
                         par.compressed, Parameters::DBTYPE_HMM_PROFILE);
  profileWriter.open();

  DBWriter headerWriter(out, par.hdr2.c_str(), par.hdr2Index.c_str(), par.threads,
                        par.compressed, Parameters::DBTYPE_GENERIC_DB);
  headerWriter.open();

  SubstitutionMatrix subMat(out, par.scoringMatrixFile.aminoacids, 2.0, 0.0);

  size_t maxElementSize = 0;
  for (size_t i = 0; i < reader.getSize(); i++) {
    maxElementSize = std::max(reader.getEntryLen(i), maxElementSize);
  }

#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = static_cast<unsigned int>(omp_get_thread_num());
#endif

    std::string sequence;
    sequence.reserve(par.maxSeqLen + 1);

    std::string header;
    header.reserve(3000);

    char *profileBuffer =
        new char[maxElementSize * Sequence::PROFILE_READIN_SIZE];

#pragma omp for schedule(dynamic, 1)
    for (size_t i = 0; i < reader.getSize(); i++) {
      char *data = reader.getData(i, thread_idx);
      size_t elementSize = 0;
      parseHMM(out, data, &sequence, &header, profileBuffer, &elementSize, i,
               &subMat);

      profileWriter.writeData(profileBuffer, elementSize, i, thread_idx);
      headerWriter.writeData(header.c_str(), header.length(), i, thread_idx);
      header.clear();
      sequence.clear();
    }
    delete[] profileBuffer;
  }
  headerWriter.close(true);
  profileWriter.close(true);
  reader.close();

  return EXIT_SUCCESS;
}
