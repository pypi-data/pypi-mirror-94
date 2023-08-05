#include <mmseqs/commons/dBReader.h>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/commons/orf.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/translateNucl.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

int translatenucs(mmseqs_output* out, Parameters& par) {
  //    Parameters& par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  DBReader<unsigned int> reader(
      out, par.db1.c_str(), par.db1Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
  reader.open(DBReader<unsigned int>::LINEAR_ACCCESS);

  bool addOrfStop = par.addOrfStop;
  DBReader<unsigned int>* header = NULL;
  if (addOrfStop == true) {
    header = new DBReader<unsigned int>(
        out, par.hdr1.c_str(), par.hdr1Index.c_str(), par.threads,
        DBReader<unsigned int>::USE_INDEX | DBReader<unsigned int>::USE_DATA);
    header->open(DBReader<unsigned int>::NOSORT);
  }

  size_t entries = reader.getSize();
  unsigned int localThreads =
      std::max(std::min((unsigned int)par.threads, (unsigned int)entries), 1u);

  DBWriter writer(out, par.db2.c_str(), par.db2Index.c_str(), localThreads,
                  par.compressed, Parameters::DBTYPE_AMINO_ACIDS);
  writer.open();

  Log::Progress progress(entries);
  TranslateNucl translateNucl(
      out, static_cast<TranslateNucl::GenCode>(par.translationTable));
#pragma omp parallel num_threads(localThreads)
  {
    int thread_idx = 0;
#ifdef OPENMP
    thread_idx = omp_get_thread_num();
#endif

    char* aa = new char[(par.maxSeqLen + 1) + 3 + 1];
#pragma omp for schedule(dynamic, 5)
    for (size_t i = 0; i < entries; ++i) {
      progress.updateProgress();

      unsigned int key = reader.getDbKey(i);
      char* data = reader.getData(i, thread_idx);
      if (*data == '\0') {
        continue;
      }

      bool addStopAtStart = false;
      bool addStopAtEnd = false;
      if (addOrfStop == true) {
        char* headData = header->getDataByDBKey(key, thread_idx);
        Orf::SequenceLocation loc = Orf::parseOrfHeader(headData);
        addStopAtStart = !(loc.hasIncompleteStart);
        addStopAtEnd = !(loc.hasIncompleteEnd);
      }

      // 190344_chr1_1_129837240_129837389_3126_JFOA01000125.1 Prochlorococcus
      // sp. scB245a_521M10 contig_244, whole genome shotgun sequence  [Orf: 1,
      // 202, -1, 1, 0]
      // ignore null char at the end
      // needs to be int in order to be able to check
      size_t length = reader.getEntryLen(i) - 1;
      if ((data[length] != '\n' && length % 3 != 0) &&
          (data[length - 1] == '\n' && (length - 1) % 3 != 0)) {
        key, length,
        out->warn("Nucleotide sequence entry {} length ({}) is not divisible by three. Adjust length to (length={})", key, length, length - (length % 3));
        length = length - (length % 3);
      }

      if (length < 3) {
        out->warn("Nucleotide sequence entry {} length ({}) is too short. Skipping entry", key, length);
        continue;
      }

      if (length > (3 * par.maxSeqLen)) {
        out->warn("Nucleotide sequence entry {} length ({}) is too long. Trimming entry", key, length);
        length = (3 * par.maxSeqLen);
      }

      char* writeAA;
      if (addStopAtStart) {
        aa[0] = '*';
        writeAA = aa + 1;
      } else {
        writeAA = aa;
      }
      translateNucl.translate(writeAA, data, length);

      if (addStopAtEnd && writeAA[(length / 3) - 1] != '*') {
        writeAA[length / 3] = '*';
        writeAA[length / 3 + 1] = '\n';
      } else {
        addStopAtEnd = false;
        writeAA[length / 3] = '\n';
      }

      writer.writeData(aa, (length / 3) + 1 + addStopAtStart + addStopAtEnd,
                       key, thread_idx);
    }
    delete[] aa;
  }
  writer.close(true);
  DBReader<unsigned int>::softlinkDb(out, par.db1, par.db2,
                                     DBFiles::SEQUENCE_ANCILLARY);

  if (addOrfStop == true) {
    header->close();
  }
  reader.close();

  return EXIT_SUCCESS;
}
