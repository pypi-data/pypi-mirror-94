#include <mmseqs/clustering/clusteringAlgorithms.h>
#include <mmseqs/clustering/alignmentSymmetry.h>
#include <mmseqs/output.h>
#include <mmseqs/commons/timer.h>
#include <mmseqs/commons/util.h>
#include <mmseqs/commons/fastSort.h>

#include <algorithm>
#include <climits>
#include <queue>
#include <unordered_map>

#ifdef OPENMP
#include <omp.h>
#endif

ClusteringAlgorithms::ClusteringAlgorithms(mmseqs_output* output, DBReader<unsigned int> *seqDbr,
                                           DBReader<unsigned int> *alnDbr,
                                           int threads, int scoretype,
                                           int maxiterations): out(output) {
  this->seqDbr = seqDbr;
  if (seqDbr->getSize() != alnDbr->getSize()) {
    out->failure("Sequence db size != result db size");
  }
  this->alnDbr = alnDbr;
  this->dbSize = alnDbr->getSize();
  this->threads = threads;
  this->scoretype = scoretype;
  this->maxiterations = maxiterations;
  /// time
  this->clustersizes = new int[dbSize];
  std::fill_n(clustersizes, dbSize, 0);
}

ClusteringAlgorithms::~ClusteringAlgorithms() { delete[] clustersizes; }

std::pair<unsigned int, unsigned int> *ClusteringAlgorithms::execute(int mode) {
  // init data

  unsigned int *assignedcluster = new (std::nothrow) unsigned int[dbSize];
  Util::checkAllocation(out, assignedcluster,
                        "Can not allocate assignedcluster memory in "
                        "ClusteringAlgorithms::execute");
  std::fill_n(assignedcluster, dbSize, UINT_MAX);

  // time
  if (mode == 4 || mode == 2) {
    greedyIncrementalLowMem(assignedcluster);
  } else {
    size_t elementCount = 0;
#pragma omp parallel reduction(+ : elementCount)
    {
      int thread_idx = 0;
#ifdef OPENMP
      thread_idx = omp_get_thread_num();
#endif
#pragma omp for schedule(dynamic, 10)
      for (size_t i = 0; i < alnDbr->getSize(); i++) {
        const char *data = alnDbr->getData(i, thread_idx);
        const size_t dataSize = alnDbr->getEntryLen(i);
        elementCount += (*data == '\0') ? 1 : Util::countLines(data, dataSize);
      }
    }
    unsigned int *elements = new (std::nothrow) unsigned int[elementCount];
    Util::checkAllocation(
        out,
        elements,
        "Can not allocate elements memory in ClusteringAlgorithms::execute");
    unsigned int **elementLookupTable =
        new (std::nothrow) unsigned int *[dbSize];
    Util::checkAllocation(out, elementLookupTable,
                          "Can not allocate elementLookupTable memory in "
                          "ClusteringAlgorithms::execute");
    unsigned short **scoreLookupTable =
        new (std::nothrow) unsigned short *[dbSize];
    Util::checkAllocation(out, scoreLookupTable,
                          "Can not allocate scoreLookupTable memory in "
                          "ClusteringAlgorithms::execute");
    unsigned short *score = NULL;
    size_t *elementOffsets = new (std::nothrow) size_t[dbSize + 1];
    Util::checkAllocation(out, elementOffsets,
                          "Can not allocate elementOffsets memory in "
                          "ClusteringAlgorithms::execute");
    elementOffsets[dbSize] = 0;
    short *bestscore = new (std::nothrow) short[dbSize];
    Util::checkAllocation(
        out,
        bestscore,
        "Can not allocate bestscore memory in ClusteringAlgorithms::execute");
    std::fill_n(bestscore, dbSize, SHRT_MIN);

    readInClusterData(elementLookupTable, elements, scoreLookupTable, score,
                      elementOffsets, elementCount);
    ClusteringAlgorithms::initClustersizes();
    if (mode == 1) {
      setCover(elementLookupTable, scoreLookupTable, assignedcluster, bestscore,
               elementOffsets);
    } else if (mode == 3) {
      out->info("Clustering: connected component mode");
      for (int cl_size = dbSize - 1; cl_size >= 0; cl_size--) {
        unsigned int representative = sorted_clustersizes[cl_size];
        if (assignedcluster[representative] == UINT_MAX) {
          assignedcluster[representative] = representative;
          std::queue<int> myqueue;
          myqueue.push(representative);
          std::queue<int> iterationcutoffs;
          iterationcutoffs.push(0);
          // delete clusters of members;
          while (!myqueue.empty()) {
            int currentid = myqueue.front();
            int iterationcutoff = iterationcutoffs.front();
            assignedcluster[currentid] = representative;
            myqueue.pop();
            iterationcutoffs.pop();
            size_t elementSize =
                (elementOffsets[currentid + 1] - elementOffsets[currentid]);
            for (size_t elementId = 0; elementId < elementSize; elementId++) {
              unsigned int elementtodelete =
                  elementLookupTable[currentid][elementId];
              if (assignedcluster[elementtodelete] == UINT_MAX &&
                  iterationcutoff < maxiterations) {
                myqueue.push(elementtodelete);
                iterationcutoffs.push((iterationcutoff + 1));
              }
              assignedcluster[elementtodelete] = representative;
            }
          }
        }
      }
    }
    // delete unnecessary datastructures
    delete[] sorted_clustersizes;
    delete[] clusterid_to_arrayposition;
    delete[] borders_of_set;

    delete[] elementLookupTable;
    delete[] elements;
    delete[] elementOffsets;
    delete[] scoreLookupTable;
    delete[] score;
    delete[] bestscore;
  }

  std::pair<unsigned int, unsigned int> *assignment =
      new std::pair<unsigned int, unsigned int>[dbSize];
#pragma omp parallel
  {
#pragma omp for schedule(static)
    for (size_t i = 0; i < dbSize; i++) {
      if (assignedcluster[i] == UINT_MAX) {
        out->error("There must be an error: {} ({}) is not assigned to a cluster", seqDbr->getDbKey(i), i);
        continue;
      }

      assignment[i].first = seqDbr->getDbKey(assignedcluster[i]);
      assignment[i].second = seqDbr->getDbKey(i);
    }
  }
  SORT_PARALLEL(assignment, assignment + dbSize);
  delete[] assignedcluster;
  return assignment;
}

void ClusteringAlgorithms::initClustersizes() {
  unsigned int *setsize_abundance = new unsigned int[maxClustersize + 1];

  std::fill_n(setsize_abundance, maxClustersize + 1, 0);
  // count how often a set size occurs
  for (unsigned int i = 0; i < dbSize; ++i) {
    setsize_abundance[clustersizes[i]]++;
  }
  // compute offsets
  borders_of_set = new unsigned int[maxClustersize + 1];
  borders_of_set[0] = 0;
  for (unsigned int i = 1; i < maxClustersize + 1; ++i) {
    borders_of_set[i] = borders_of_set[i - 1] + setsize_abundance[i - 1];
  }
  // fill array
  sorted_clustersizes = new (std::nothrow) unsigned int[dbSize + 1];
  Util::checkAllocation(out, sorted_clustersizes,
                        "Can not allocate sorted_clustersizes memory in "
                        "ClusteringAlgorithms::initClustersizes");

  std::fill_n(sorted_clustersizes, dbSize + 1, 0);
  clusterid_to_arrayposition = new (std::nothrow) unsigned int[dbSize + 1];
  Util::checkAllocation(out, clusterid_to_arrayposition,
                        "Can not allocate sorted_clustersizes memory in "
                        "ClusteringAlgorithms::initClustersizes");

  std::fill_n(clusterid_to_arrayposition, dbSize + 1, 0);
  // reuse setsize_abundance as offset counter
  std::fill_n(setsize_abundance, maxClustersize + 1, 0);
  for (unsigned int i = 0; i < dbSize; ++i) {
    unsigned int position =
        borders_of_set[clustersizes[i]] + setsize_abundance[clustersizes[i]];
    sorted_clustersizes[position] = i;
    clusterid_to_arrayposition[i] = position;
    setsize_abundance[clustersizes[i]]++;
  }
  delete[] setsize_abundance;
}

void ClusteringAlgorithms::removeClustersize(unsigned int clusterid) {
  clustersizes[clusterid] = 0;
  sorted_clustersizes[clusterid_to_arrayposition[clusterid]] = UINT_MAX;
  clusterid_to_arrayposition[clusterid] = UINT_MAX;
}

void ClusteringAlgorithms::decreaseClustersize(unsigned int clusterid) {
  const unsigned int oldposition = clusterid_to_arrayposition[clusterid];
  const unsigned int newposition = borders_of_set[clustersizes[clusterid]];
  const unsigned int swapid = sorted_clustersizes[newposition];
  if (swapid != UINT_MAX) {
    clusterid_to_arrayposition[swapid] = oldposition;
  }
  sorted_clustersizes[oldposition] = swapid;

  sorted_clustersizes[newposition] = clusterid;
  clusterid_to_arrayposition[clusterid] = newposition;
  borders_of_set[clustersizes[clusterid]]++;
  clustersizes[clusterid]--;
}

void ClusteringAlgorithms::setCover(unsigned int **elementLookupTable,
                                    unsigned short **elementScoreLookupTable,
                                    unsigned int *assignedcluster,
                                    short *bestscore,
                                    size_t *newElementOffsets) {
  for (int64_t cl_size = dbSize - 1; cl_size >= 0; cl_size--) {
    const unsigned int representative = sorted_clustersizes[cl_size];
    if (representative == UINT_MAX) {
      continue;
    }
    removeClustersize(representative);
    assignedcluster[representative] = representative;

    // Delete clusters of members;
    size_t elementSize = (newElementOffsets[representative + 1] -
                          newElementOffsets[representative]);
    for (size_t elementId = 0; elementId < elementSize; elementId++) {
      const unsigned int elementtodelete =
          elementLookupTable[representative][elementId];
      // float seqId = elementScoreTable[representative][elementId];
      const short seqId = elementScoreLookupTable[representative][elementId];

      // Be careful of this criteria
      if (seqId > bestscore[elementtodelete]) {
        assignedcluster[elementtodelete] = representative;
        bestscore[elementtodelete] = seqId;
      }
      if (elementtodelete == representative) {
        continue;
      }
      if (clustersizes[elementtodelete] < 1) {
        continue;
      }
      removeClustersize(elementtodelete);
    }

    for (size_t elementId = 0; elementId < elementSize; elementId++) {
      bool representativefound = false;
      const unsigned int elementtodelete =
          elementLookupTable[representative][elementId];
      const unsigned int currElementSize =
          (newElementOffsets[elementtodelete + 1] -
           newElementOffsets[elementtodelete]);
      if (elementtodelete == representative) {
        clustersizes[elementtodelete] = -1;
        continue;
      }
      if (clustersizes[elementtodelete] < 0) {
        continue;
      }
      clustersizes[elementtodelete] = -1;
      // decrease clustersize of sets that contain the element
      for (size_t elementId2 = 0; elementId2 < currElementSize; elementId2++) {
        const unsigned int elementtodecrease =
            elementLookupTable[elementtodelete][elementId2];
        if (representative == elementtodecrease) {
          representativefound = true;
        }
        if (clustersizes[elementtodecrease] == 1) {
          out->error("There must be an error: {} deleted from {} that now is empty, but not assigned to a cluster", seqDbr->getDbKey(elementtodelete), seqDbr->getDbKey(elementtodecrease));
        } else if (clustersizes[elementtodecrease] > 0) {
          decreaseClustersize(elementtodecrease);
        }
      }
      if (!representativefound) {
        out->error("Error with cluster: {} is not contained in set: {}", seqDbr->getDbKey(representative), seqDbr->getDbKey(elementtodelete));
      }
    }
  }
}

void ClusteringAlgorithms::greedyIncrementalLowMem(
    unsigned int *assignedcluster) {
  // two step clustering
  // 1.) we define the rep. sequences by minimizing the ids (smaller ID = longer
  // sequence) 2.) we correct maybe wrong assigned sequence by checking if the
  // assigned sequence is really a rep. seq.
  //     if they are not make them rep. seq.
#pragma omp parallel
  {
    int thread_idx = 0;
#ifdef OPENMP
    thread_idx = omp_get_thread_num();
#endif
#pragma omp for schedule(dynamic, 1000)
    for (size_t i = 0; i < dbSize; i++) {
      unsigned int clusterKey = seqDbr->getDbKey(i);
      unsigned int clusterId = seqDbr->getId(clusterKey);

      // try to set your self as cluster centriod
      // if some other cluster covered
      unsigned int targetId;
      __atomic_load(&assignedcluster[clusterId], &targetId, __ATOMIC_RELAXED);
      do {
        if (targetId <= clusterId) break;
      } while (!__atomic_compare_exchange(&assignedcluster[clusterId],
                                          &targetId, &clusterId, false,
                                          __ATOMIC_RELAXED, __ATOMIC_RELAXED));

      const size_t alnId = alnDbr->getId(clusterKey);
      char *data = alnDbr->getData(alnId, thread_idx);

      while (*data != '\0') {
        char dbKey[255 + 1];
        Util::parseKey(data, dbKey);
        const unsigned int key = (unsigned int)strtoul(dbKey, NULL, 10);

        unsigned int currElement = seqDbr->getId(key);
        unsigned int targetId;

        __atomic_load(&assignedcluster[currElement], &targetId,
                      __ATOMIC_RELAXED);
        do {
          if (targetId <= clusterId) break;
        } while (!__atomic_compare_exchange(
            &assignedcluster[currElement], &targetId, &clusterId, false,
            __ATOMIC_RELAXED, __ATOMIC_RELAXED));

        if (currElement == UINT_MAX || currElement > seqDbr->getSize()) {
          out->failure("Element {} contained in some alignment list, but not contained in the sequence database.", dbKey);
        }
        data = Util::skipLine(data);
      }
    }
  }

  // correct edges that are not assigned properly
  for (size_t id = 0; id < dbSize; ++id) {
    unsigned int assignedClusterId = assignedcluster[id];
    // check if the assigned clusterid is a rep. sequence
    // if not, make it a rep. seq. again
    if (assignedcluster[assignedClusterId] != assignedClusterId) {
      assignedcluster[assignedClusterId] = assignedClusterId;
    }
  }
}

void ClusteringAlgorithms::readInClusterData(unsigned int **elementLookupTable,
                                             unsigned int *&elements,
                                             unsigned short **scoreLookupTable,
                                             unsigned short *&scores,
                                             size_t *elementOffsets,
                                             size_t totalElementCount) {
  Timer timer;
#pragma omp parallel
  {
    int thread_idx = 0;
#ifdef OPENMP
    thread_idx = omp_get_thread_num();
#endif
#pragma omp for schedule(dynamic, 1000)
    for (size_t i = 0; i < dbSize; i++) {
      const unsigned int clusterId = seqDbr->getDbKey(i);
      const size_t alnId = alnDbr->getId(clusterId);
      const char *data = alnDbr->getData(alnId, thread_idx);
      const size_t dataSize = alnDbr->getEntryLen(alnId);
      elementOffsets[i] =
          (*data == '\0') ? 1 : Util::countLines(data, dataSize);
    }
  }

  // make offset table
  AlignmentSymmetry::computeOffsetFromCounts(out, elementOffsets, dbSize);
  // set element edge pointers by using the offset table
  AlignmentSymmetry::setupPointers<unsigned int>(
      out, elements, elementLookupTable, elementOffsets, dbSize, totalElementCount);
  // fill elements
  AlignmentSymmetry::readInData(out, alnDbr, seqDbr, elementLookupTable, NULL, 0,
                                elementOffsets);

  out->info("Sort entries");
  AlignmentSymmetry::sortElements(out, elementLookupTable, elementOffsets, dbSize);
  out->info("Find missing connections");

  size_t *newElementOffsets = new size_t[dbSize + 1];
  memcpy(newElementOffsets, elementOffsets, sizeof(size_t) * (dbSize + 1));

  // findMissingLinks detects new possible connections and updates the
  // elementOffsets with new sizes
  const size_t symmetricElementCount = AlignmentSymmetry::findMissingLinks(
      out, elementLookupTable, newElementOffsets, dbSize, threads);
  // resize elements
  delete[] elements;
  elements = new (std::nothrow) unsigned int[symmetricElementCount];
  Util::checkAllocation(
      out, elements, "Can not allocate elements memory in readInClusterData");
  std::fill_n(elements, symmetricElementCount, UINT_MAX);
  // init score vector
  scores = new (std::nothrow) unsigned short[symmetricElementCount];
  Util::checkAllocation(out, scores,
                        "Can not allocate scores memory in readInClusterData");
  std::fill_n(scores, symmetricElementCount, 0);
  out->info("Found {} new connections", symmetricElementCount - totalElementCount);
  AlignmentSymmetry::setupPointers<unsigned int>(out, elements, elementLookupTable,
                                                 newElementOffsets, dbSize,
                                                 symmetricElementCount);
  AlignmentSymmetry::setupPointers<unsigned short>(out, scores, scoreLookupTable,
                                                   newElementOffsets, dbSize,
                                                   symmetricElementCount);
  // time
  out->info("Reconstruct initial order");
  alnDbr->remapData();  // need to free memory
  AlignmentSymmetry::readInData(out, alnDbr, seqDbr, elementLookupTable,
                                scoreLookupTable, scoretype, elementOffsets);
  alnDbr->remapData();  // need to free memory
  out->info("Add missing connections");
  AlignmentSymmetry::addMissingLinks(out, elementLookupTable, elementOffsets,
                                     newElementOffsets, dbSize,
                                     scoreLookupTable);
  maxClustersize = 0;
  for (size_t i = 0; i < dbSize; i++) {
    size_t elementCount = newElementOffsets[i + 1] - newElementOffsets[i];
    maxClustersize = std::max((unsigned int)elementCount, maxClustersize);
    clustersizes[i] = elementCount;
  }

  memcpy(elementOffsets, newElementOffsets, sizeof(size_t) * (dbSize + 1));
  delete[] newElementOffsets;
  out->info("Time for read in: {}", timer.lap());
}
