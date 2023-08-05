#ifndef NUCLEOTIDE_MATRIX_H
#define NUCLEOTIDE_MATRIX_H

#include <mmseqs/commons/substitutionMatrix.h>

class NucleotideMatrix : public SubstitutionMatrix {
 public:
  NucleotideMatrix(mmseqs_output* output, const char *scoringMatrixFileName, float bitFactor,
                   float scoreBias);

  virtual ~NucleotideMatrix();

  using BaseMatrix::getBitFactor;

  void setupLetterMapping();

  int reverseResidue(int res) { return reverseLookup[res]; }

 private:
  int *reverseLookup;
};

#endif
