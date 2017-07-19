#include "cell.hh"

#include <stdio.h>


Cell::Cell() {
  for (int i = 0; i < 2; i++)
    for (int j = 0; j < 2; j++)
      Gbytes[i][j] = Gpkts[i][j] = 0;
}

void Cell::Add(int i, int j, int p, int b) {
  Gbytes[i][j] += b / 1000000000.0;
  Gpkts[i][j] += p / 1000000000.0;
}

const char *Cell::ToString() {
  sprintf(output, "%lf (%lf) %lf (%lf) %lf (%lf) %lf (%lf)", Gpkts[0][0], Gbytes[0][0], Gpkts[0][1], Gbytes[0][1],
          Gpkts[1][0], Gbytes[1][0], Gpkts[1][1], Gbytes[1][1]);
  return output;
}
