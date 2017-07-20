#include "cell.hh"



Cell::Cell() {
  for (int i = 0; i < 2; i++)
    for (int j = 0; j < 2; j++)
      Gbytes[i][j] = Gpkts[i][j] = 0;
}

void Cell::Add(int i, int j, int p, int b) {
  Gbytes[i][j] += b / 1000000000.0;
  Gpkts[i][j] += p / 1000000000.0;
}

std::string Cell::ToString() {
  for(int i = 0; i < 2; i++){
    for(int j = 0; j < 2; j++){
      output += std::to_string(Gpkts[i][j]) + " " + std::to_string(Gbytes[i][j]) + " ";
    }
  }
  return output;
}
