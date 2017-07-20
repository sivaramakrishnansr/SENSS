//
// Created by Abdul Qadeer on 7/19/17.
//

#ifndef SENSS_COLLECTOR_H
#define SENSS_COLLECTOR_H

#include "cell.hh"
#include "config.hh"

class Collector {

 private:
  map<iprange, map<long long double, Cell>> stats;
 public:
  
};

#endif //SENSS_COLLECTOR_H
