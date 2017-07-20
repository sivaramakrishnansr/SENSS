//
// Created by Abdul Qadeer on 7/19/17.
//

#ifndef SENSS_COLLECTOR_H
#define SENSS_COLLECTOR_H

#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <map>

#include "cell.hh"
#include "config.hh"
#include "iprange.hh"
using namespace std;


class Collector {

 private:
  map<IpRange, map<long long double, Cell>> stats;
 public:
  Collector() = default;
  void ProcessClient(int cli_fd);
  void StartServer();
  void CleanUpStats();


};

#endif //SENSS_COLLECTOR_H
