#include <algorithm>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/taxonomy/ncbiTaxonomy.h>
#include <mmseqs/commons/parameters.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/output.h>

#ifdef OPENMP
#include <omp.h>
#endif

static bool compareToFirstInt(
    const std::pair<unsigned int, unsigned int> &lhs,
    const std::pair<unsigned int, unsigned int> &rhs) {
  return (lhs.first <= rhs.first);
}

int addtaxonomy(mmseqs_output *out, Parameters &par) {
  //    Parameters &par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);

  std::vector<std::pair<unsigned int, unsigned int>> mapping;
  if (FileUtil::fileExists(out, (par.db1 + "_mapping").c_str()) == false) {
    out->failure("{}_mapping does not exist. Run createtaxdb to create taxonomy mapping", par.db1);
  }
  const bool isSorted = Util::readMapping(out, par.db1 + "_mapping", mapping);
  if (isSorted == false) {
    std::stable_sort(mapping.begin(), mapping.end(), compareToFirstInt);
  }
  if (mapping.size() == 0) {
    out->failure("{}_mapping is empty. Rerun createtaxdb to recreate taxonomy mapping", par.db1);
  }
  NcbiTaxonomy *t = NcbiTaxonomy::openTaxonomy(out, par.db1);
  std::vector<std::string> ranks = NcbiTaxonomy::parseRanks(out, par.lcaRanks);

  DBReader<unsigned int> reader(
      out,
      par.db2.c_str(), par.db2Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_DATA | DBReader<unsigned int>::USE_INDEX);
  reader.open(DBReader<unsigned int>::LINEAR_ACCCESS);

  DBWriter writer(out, par.db3.c_str(), par.db3Index.c_str(), par.threads,
                  par.compressed, reader.getDbtype());
  writer.open();

  size_t taxonNotFound = 0;
  size_t deletedNodes = 0;
  Log::Progress progress(reader.getSize());
#pragma omp parallel
  {
    unsigned int thread_idx = 0;
#ifdef OPENMP
    thread_idx = (unsigned int)omp_get_thread_num();
#endif
    const char *entry[255];
    std::string result;
    result.reserve(4096);

#pragma omp for schedule(dynamic, 10) reduction(+ : deletedNodes, taxonNotFound)
    for (size_t i = 0; i < reader.getSize(); ++i) {
      progress.updateProgress();

      unsigned int key = reader.getDbKey(i);
      char *data = reader.getData(i, thread_idx);
      size_t length = reader.getEntryLen(i);

      if (length == 1) {
        continue;
      }
      std::pair<unsigned int, unsigned int> val;
      std::vector<std::pair<unsigned int, unsigned int>>::iterator mappingIt;
      if (par.pickIdFrom == Parameters::EXTRACT_QUERY) {
        val.first = key;
        mappingIt = std::upper_bound(mapping.begin(), mapping.end(), val,
                                     compareToFirstInt);
        if (mappingIt == mapping.end() || mappingIt->first != val.first) {
          taxonNotFound++;
          continue;
        }
      }

      while (*data != '\0') {
        const size_t columns = Util::getWordsOfLine(data, entry, 255);
        if (columns == 0) {
          out->warn("Empty entry: {}", i);
          data = Util::skipLine(data);
          continue;
        }
        if (par.pickIdFrom == Parameters::EXTRACT_TARGET) {
          unsigned int id = Util::fast_atoi<unsigned int>(entry[0]);
          val.first = id;
          mappingIt = std::upper_bound(mapping.begin(), mapping.end(), val,
                                       compareToFirstInt);
          if (mappingIt == mapping.end() || mappingIt->first != val.first) {
            taxonNotFound++;
            data = Util::skipLine(data);
            continue;
          }
        }
        unsigned int taxon = mappingIt->second;
        TaxonNode const *node = t->taxonNode(taxon, false);
        if (node == NULL) {
          deletedNodes++;
          data = Util::skipLine(data);
          continue;
        }
        char *nextData = Util::skipLine(data);
        size_t dataSize = nextData - data;
        result.append(data, dataSize - 1);
        result.append(1, '\t');
        result.append(SSTR(node->taxId));
        result.append(1, '\t');
        result.append(t->getString(node->rankIdx));
        result.append(1, '\t');
        result.append(t->getString(node->nameIdx));
        if (!ranks.empty()) {
          result.append(1, '\t');
          result.append(Util::implode(t->AtRanks(node, ranks), ';'));
        }
        if (par.showTaxLineage == 1) {
          result.append(1, '\t');
          result.append(t->taxLineage(node, true));
        }
        if (par.showTaxLineage == 2) {
          result.append(1, '\t');
          result.append(t->taxLineage(node, false));
        }
        result.append(1, '\n');
        data = Util::skipLine(data);
      }
      writer.writeData(result.c_str(), result.size(), key, thread_idx);
      result.clear();
    }
  }
  out->info("Taxonomy for {} entries not found and {} are deleted ", taxonNotFound, deletedNodes);
  writer.close();
  reader.close();
  delete t;
  return EXIT_SUCCESS;
}
