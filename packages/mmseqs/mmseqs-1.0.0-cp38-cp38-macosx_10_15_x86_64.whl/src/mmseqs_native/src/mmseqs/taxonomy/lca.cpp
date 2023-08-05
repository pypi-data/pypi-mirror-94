#include <algorithm>
#include <mmseqs/commons/dBWriter.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/fileUtil.h>
#include <mmseqs/alignment/matcher.h>
#include <mmseqs/taxonomy/ncbiTaxonomy.h>
#include <mmseqs/commons/parameters.h>
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

int dolca(mmseqs_output* out, Parameters& par, bool majority) {
  //    Parameters& par = Parameters::getInstance();
  //    par.parseParameters(argc, argv, command, true, 0, 0);
  NcbiTaxonomy* t = NcbiTaxonomy::openTaxonomy(out, par.db1);

  std::vector<std::pair<unsigned int, unsigned int>> mapping;
  if (FileUtil::fileExists(out, std::string(par.db1 + "_mapping").c_str()) ==
      false) {
    out->failure("{}_mapping does not exist. Please create the taxonomy mapping", par.db1);
  }
  bool isSorted = Util::readMapping(out, par.db1 + "_mapping", mapping);
  if (isSorted == false) {
    std::stable_sort(mapping.begin(), mapping.end(), compareToFirstInt);
  }

  DBReader<unsigned int> reader(
      out,
      par.db2.c_str(), par.db2Index.c_str(), par.threads,
      DBReader<unsigned int>::USE_DATA | DBReader<unsigned int>::USE_INDEX);
  reader.open(DBReader<unsigned int>::LINEAR_ACCCESS);

  DBWriter writer(out, par.db3.c_str(), par.db3Index.c_str(), par.threads,
                  par.compressed, Parameters::DBTYPE_TAXONOMICAL_RESULT);
  writer.open();

  std::vector<std::string> ranks = NcbiTaxonomy::parseRanks(out, par.lcaRanks);

  // a few NCBI taxa are blacklisted by default, they contain unclassified
  // sequences (e.g. metagenomes) or other sequences (e.g. plasmids) if we do
  // not remove those, a lot of sequences would be classified as Root, even
  // though they have a sensible LCA
  std::vector<TaxID> blacklist;
  std::vector<std::string> splits = Util::split(par.blacklist, ",");
  for (size_t i = 0; i < splits.size(); ++i) {
    TaxID taxon = Util::fast_atoi<int>(splits[i].c_str());
    if (taxon == 0) {
      out->warn("Cannot block root taxon 0");
      continue;
    }
    if (t->nodeExists(taxon) == false) {
      out->warn("Ignoring missing blocked taxon {}", taxon);
      continue;
    }

    const char* split;
    if ((split = strchr(splits[i].c_str(), ':')) != NULL) {
      const char* name = split + 1;
      const TaxonNode* node = t->taxonNode(taxon, false);
      if (node == NULL) {
        out->warn("Ignoring missing blocked taxon {}", taxon);
        continue;
      }
      const char* nodeName = t->getString(node->nameIdx);
      if (strcmp(nodeName, name) != 0) {
        out->warn("Node name '{}' does not match to be blocked name '{}'", name, nodeName);
        continue;
      }
    }
    blacklist.emplace_back(taxon);
  }

  // will be used when no hits
  std::string noTaxResult = "0\tno rank\tunclassified";
  if (!ranks.empty()) {
    noTaxResult += '\t';
  }
  if (par.showTaxLineage > 0) {
    noTaxResult += '\t';
  }
  noTaxResult += '\n';

  size_t taxonNotFound = 0;
  size_t found = 0;
  Log::Progress progress(reader.getSize());
#pragma omp parallel
  {
    const char* entry[255];
    std::string result;
    result.reserve(4096);
    unsigned int thread_idx = 0;

#ifdef OPENMP
    thread_idx = (unsigned int)omp_get_thread_num();
#endif

#pragma omp for schedule(dynamic, 10) reduction(+ : taxonNotFound, found)
    for (size_t i = 0; i < reader.getSize(); ++i) {
      progress.updateProgress();

      unsigned int key = reader.getDbKey(i);
      char* data = reader.getData(i, thread_idx);
      size_t length = reader.getEntryLen(i);

      std::vector<int> taxa;
      std::vector<WeightedTaxHit> weightedTaxa;
      while (*data != '\0') {
        TaxID taxon;
        unsigned int id;
        std::pair<unsigned int, unsigned int> val;
        std::vector<std::pair<unsigned int, unsigned int>>::iterator mappingIt;
        const size_t columns = Util::getWordsOfLine(data, entry, 255);
        data = Util::skipLine(data);
        if (columns == 0) {
          out->warn("Empty entry: {}!", i);
          continue;
        }

        id = Util::fast_atoi<unsigned int>(entry[0]);
        val.first = id;
        mappingIt = std::upper_bound(mapping.begin(), mapping.end(), val,
                                     compareToFirstInt);

        if (mappingIt == mapping.end() || mappingIt->first != val.first) {
          // TODO: Check which taxa were not found
          taxonNotFound += 1;
          continue;
        }
        found++;
        taxon = mappingIt->second;

        // remove blacklisted taxa
        bool isBlacklisted = false;
        for (size_t j = 0; j < blacklist.size(); ++j) {
          if (blacklist[j] == 0) {
            continue;
          }
          if (t->IsAncestor(blacklist[j], taxon)) {
            isBlacklisted = true;
            break;
          }
        }

        if (isBlacklisted == false) {
          if (majority) {
            float weight = FLT_MAX;
            if (par.voteMode == Parameters::AGG_TAX_MINUS_LOG_EVAL) {
              if (columns <= 3) {
                out->failure("No alignment result for taxon {} found", taxon);
              }
              weight = strtod(entry[3], NULL);
            } else if (par.voteMode == Parameters::AGG_TAX_SCORE) {
              if (columns <= 1) {
                out->failure("No alignment result for taxon {} found", taxon);
              }
              weight = strtod(entry[1], NULL);
            }
            weightedTaxa.emplace_back(out, taxon, weight, par.voteMode);
          } else {
            taxa.emplace_back(taxon);
          }
        }
      }

      if (length == 1) {
        writer.writeData(noTaxResult.c_str(), noTaxResult.size(), key,
                         thread_idx);
        continue;
      }

      TaxonNode const* node = NULL;
      if (majority) {
        WeightedTaxResult result =
            t->weightedMajorityLCA(weightedTaxa, par.majorityThr);
        node = t->taxonNode(result.taxon, false);
      } else {
        node = t->LCA(taxa);
      }
      if (node == NULL) {
        writer.writeData(noTaxResult.c_str(), noTaxResult.size(), key,
                         thread_idx);
        continue;
      }

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
      writer.writeData(result.c_str(), result.size(), key, thread_idx);
      result.clear();
    }
  }
  out->info("Taxonomy for {} out of {} entries not found ", taxonNotFound, taxonNotFound + found);
  writer.close();
  reader.close();
  delete t;

  return EXIT_SUCCESS;
}

int lca(mmseqs_output* out, Parameters& par) { return dolca(out, par, false); }

int majoritylca(mmseqs_output* out, Parameters& par) {
  return dolca(out, par, true);
}
