#ifndef __RECORDS_HH
#define __RECORDS_HH

#include <map>
#include "cell.hh"
#include "iprange.hh"
#include "flow.hh"

using namespace std;

class records
{
public:
  records();
  void insert(iprange, int, int, int, int);
  
  map<iprange,cell> stats;
};

#endif
