#ifndef __CELL_HH
#define __CELL_HH


class cell
{
public:
  cell();
  void add(int, int, int, int);
  const char* tostr();  

  double Gbytes[2][2];
  double Gpkts[2][2];
  char output[100];
};
  

#endif
