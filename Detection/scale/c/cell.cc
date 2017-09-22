#include "cell.h"

Cell::Cell() {
  for (int i = 0; i < 2; i++)
    for (int j = 0; j < 2; j++)
      bytes[i][j] = pkts[i][j] = 0;
}

void Cell::Add(int i, int j, int p, int b) {
  // i = issrc, j = isreq = !succ
  // cell[0][0] - we are receiving response
  // cell[0][1] - we are receiving request
  // cell[1][0] - we are sending response
  // cell[1][1] - we are sending request
  // detection of attack on us - cell[0][1]/cell[1][0] if >> 1 there
  // is an attack - pkts
  // detection of attack on others - cell[1][1]/cell[0][0] if >> 1 we may
  // be part of attack - pkts
  bytes[i][j] += b / 1000000000.0;
  pkts[i][j] += p / 1000000000.0;
}

std::string Cell::ToString() {
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 2; j++) {
      output += std::to_string(pkts[i][j]) + " " + std::to_string(bytes[i][j]) + " ";
    }
  }
  return output;
}
