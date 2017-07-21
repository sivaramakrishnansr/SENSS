#ifndef __RECORDS_HH
#define __RECORDS_HH

#include <map>
#include "cell.h"
#include "iprange.h"
#include "flow.h"
#include "config.h"

using namespace std;

class FlowRecord {
 public:

  void Update(const Flow &, int, int);

  void Report(double);

  int Size();

  map<IpRange,Cell> stats;
};

#endif
