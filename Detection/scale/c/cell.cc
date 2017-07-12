#include "cell.hh"

cell::cell()
{
  for (int i=0; i<2; i++)
    for (int j=0; j<2; j++)
      Gbytes[i][j] = Gpkts[i][j] = 0;
}

void cell::add(int i, int j, int p, int b)
{
  Gbytes[i][j] += b/1000000000.0;
  Gpkts[i][j] += p/1000000000.0;
}
