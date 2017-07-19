#ifndef __CELL_HH
#define __CELL_HH

class Cell {
 public:
  Cell();

  void Add(int, int, int, int);

  const char *ToString();

  double Gbytes[2][2];
  double Gpkts[2][2];
  char output[100];
};

#endif
