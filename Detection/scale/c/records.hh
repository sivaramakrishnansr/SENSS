#ifndef __RECORDS_HH
#define __RECORDS_HH

#include <map>
#include "cell.hh"
#include "iprange.hh"
#include "flow.hh"
#include "config.hh"

using namespace std;

class FlowRecord {
 public:

  void Update(const Flow &, int, int);

  void Report(double);

  int Size();

  map<IpRange,Cell> stats;
};

#endif
