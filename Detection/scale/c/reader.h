//
// Created by Abdul Qadeer on 7/20/17.
//

#ifndef SENSS_READER_H
#define SENSS_READER_H

#include <map>

#include "flow.h"
#include "iprange.h"

class Reader {

 public:
  static int clifd;
  std::map<IpRange, int> blocks;

  void ReadFlow(char *buffer);
  void ProcessFlow();
  void Report(double time);
  void ProcessFlowHelper(Flow f);
  void LoadBlocks();
  void ConnectClient(const char *servaddr);
};

#endif //SENSS_READER_H
