#ifndef __CELL_HH
#define __CELL_HH
#include <string>

/*
 * This class stores the number of Giga bytes, Giga packets that are received (per some time stamp per some IP block)
 * The 2D arrays are structured as follows:
 *      Resp  Req
 * Dst
 * Src
 *
 *
 */
class Cell {
 public:
  Cell();

  void Add(int, int, int, int);

  std::string ToString();

  double bytes[2][2];
  double pkts[2][2];
  std::string output;
};

#endif
