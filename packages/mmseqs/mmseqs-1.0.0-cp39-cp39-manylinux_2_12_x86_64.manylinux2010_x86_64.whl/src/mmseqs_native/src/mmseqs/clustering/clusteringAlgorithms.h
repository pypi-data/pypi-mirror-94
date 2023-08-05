//
// Created by lars on 08.06.15.
//

#ifndef MMSEQS_CLUSTERINGALGORITHMS_H
#define MMSEQS_CLUSTERINGALGORITHMS_H

#include <list>
#include <set>
#include <unordered_map>
#include <vector>

#include <mmseqs/commons/dBReader.h>

class ClusteringAlgorithms {
 public:
  ClusteringAlgorithms(mmseqs_output* output, DBReader<unsigned int> *seqDbr,
                       DBReader<unsigned int> *alnDbr, int threads,
                       int scoretype, int maxiterations);
  ~ClusteringAlgorithms();
  std::pair<unsigned int, unsigned int> *execute(int mode);

 private:
  mmseqs_output* out;

  DBReader<unsigned int> *seqDbr;

  DBReader<unsigned int> *alnDbr;

  int threads;
  int scoretype;
  // datastructures
  unsigned int maxClustersize;
  unsigned int dbSize;
  int *clustersizes;
  unsigned int *sorted_clustersizes;
  unsigned int *clusterid_to_arrayposition;
  unsigned int *borders_of_set;

  // methods

  void initClustersizes();

  void removeClustersize(unsigned int clusterid);

  void decreaseClustersize(unsigned int clusterid);
  // for connected component
  int maxiterations;

  void setCover(unsigned int **elementLookup,
                unsigned short **elementScoreLookupTable,
                unsigned int *assignedcluster, short *bestscore,
                size_t *offsets);

  void greedyIncremental(unsigned int **elementLookupTable,
                         size_t *elementOffsets, size_t n,
                         unsigned int *assignedcluster);

  void greedyIncrementalLowMem(unsigned int *assignedcluster);

  void readInClusterData(unsigned int **elementLookupTable,
                         unsigned int *&elements,
                         unsigned short **scoreLookupTable,
                         unsigned short *&scores, size_t *elementOffsets,
                         size_t totalElementCount);
};

#endif  // MMSEQS_CLUSTERINGALGORITHMS_H
