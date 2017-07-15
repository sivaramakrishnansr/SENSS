#ifndef __RECORDS_HH
#define __RECORDS_HH

#include <map>
#include "cell.hh"
#include "iprange.hh"
#include "flow.hh"
#include "config.hh"

using namespace std;

class records
{
public:
  records();
  void update(const flow&, int, int);
  void report(double);
  int size();
  
  cell** stats;
};

#endif
