#include <algorithm>
#include <map>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/taxonomy/ncbiTaxonomy.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/taxonomy/taxonomyExpression.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

static bool compareToFirstInt(
    const std::pair<unsigned int, unsigned int>& lhs,
    const std::pair<unsigned int, unsigned int>& rhs) {
  return (lhs.first <= rhs.first);
}

int filtertaxseqdb(mmseqs_output* out, Parameters& par) {
  //    Parameters& par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  // open mapping (dbKey to taxid)
  std::vector<std::pair<unsigned int, unsigned int>> mapping;
  if (FileUtil::fileExists(out, std::string(par.db1 + "_mapping").c_str()) ==
      false) {
    out->failure("{}_mapping does not exist. Please create the taxonomy mapping", par.db1);
  }
  bool isSorted = Util::readMapping(out, par.db1 + "_mapping", mapping);
  if (isSorted == false) {
    std::stable_sort(mapping.begin(), mapping.end(), compareToFirstInt);
  }

  // open taxonomy - evolutionary relationships amongst taxa
  NcbiTaxonomy* t = NcbiTaxonomy::openTaxonomy(out, par.db1);

  DBReader<unsigned int> reader(
      out,
      par.db1.c_str(), par.db1Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_DATA | DBReader<unsigned int>::USE_INDEX);
  reader.open(DBReader<unsigned int>::LINEAR_ACCCESS);
  const bool isCompressed = reader.isCompressed();

  DBWriter writer(out, par.db2.c_str(), par.db2Index.c_str(), par.threads, 0,
                  Parameters::DBTYPE_OMIT_FILE);
  writer.open();

  // a few NCBI taxa are blacklisted by default, they contain unclassified
  // sequences (e.g. metagenomes) or other sequences (e.g. plasmids) if we do
  // not remove those, a lot of sequences would be classified as Root, even
  // though they have a sensible LCA

  Log::Progress progress(reader.getSize());

  out->info("Computing LCA");
#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = (unsigned int)omp_get_thread_num();
#endif
    TaxonomyExpression taxonomyExpression(par.taxonList, *t);
#pragma omp for schedule(dynamic, 10)
    for (size_t i = 0; i < reader.getSize(); ++i) {
      progress.updateProgress();

      unsigned int key = reader.getDbKey(i);
      size_t offset = reader.getOffset(i);
      size_t length = reader.getEntryLen(i);
      unsigned int taxon = 0;

      // match dbKey to its taxon based on mapping
      std::pair<unsigned int, unsigned int> val;
      val.first = key;
      std::vector<std::pair<unsigned int, unsigned int>>::iterator mappingIt;
      mappingIt = std::upper_bound(mapping.begin(), mapping.end(), val,
                                   compareToFirstInt);
      if (mappingIt == mapping.end() || mappingIt->first != val.first) {
        taxon = 0;
      } else {
        taxon = mappingIt->second;
      }

      // if taxon is a descendent of the requested taxid, it will be retained.
      // e.g. if in taxonomyExpression taxid=2 (bacteria) and taxon=562 (E.coli)
      // then the check will return "true" cause taxon is descendent of taxid
      if (taxonomyExpression.isAncestor(taxon)) {
        if (par.subDbMode == Parameters::SUBDB_MODE_SOFT) {
          writer.writeIndexEntry(key, offset, length, thread_idx);
        } else {
          char* data = reader.getDataUncompressed(i);
          size_t originalLength = reader.getEntryLen(i);
          size_t entryLength =
              std::max(originalLength, static_cast<size_t>(1)) - 1;

          if (isCompressed) {
            // copy also the null byte since it contains the information if
            // compressed or not
            entryLength = *(reinterpret_cast<unsigned int*>(data)) +
                          sizeof(unsigned int) + 1;
            writer.writeData(data, entryLength, key, thread_idx, false, false);
          } else {
            writer.writeData(data, entryLength, key, thread_idx, true, false);
          }
          writer.writeIndexEntry(key, writer.getStart(thread_idx),
                                 originalLength, thread_idx);
        }
      }
    }
  };
  out->info("");

  writer.close(true);
  if (par.subDbMode == Parameters::SUBDB_MODE_SOFT) {
    DBReader<unsigned int>::softlinkDb(out, par.db1, par.db2,
                                       DBFiles::SEQUENCE_NO_DATA_INDEX);
  } else {
    DBWriter::writeDbtypeFile(out, par.db2.c_str(), reader.getDbtype(),
                              isCompressed);
    DBReader<unsigned int>::softlinkDb(out, par.db1, par.db2,
                                       DBFiles::SEQUENCE_ANCILLARY);
  }

  reader.close();
  delete t;

  return EXIT_SUCCESS;
}
