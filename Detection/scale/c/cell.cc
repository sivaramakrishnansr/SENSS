#include "cell.h"

Cell::Cell() {
  for (int i = 0; i < 2; i++)
    for (int j = 0; j < 2; j++)
      bytes[i][j] = pkts[i][j] = 0;
}

void Cell::Add(int i, int j, int p, int b) {
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
