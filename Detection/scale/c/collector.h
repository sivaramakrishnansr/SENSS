//
// Created by Abdul Qadeer on 7/19/17.
//

#ifndef SENSS_COLLECTOR_H
#define SENSS_COLLECTOR_H

#include <queue>
#include <mutex>
#include "iprange.h"
#include "map.pb.h"
using namespace std;

typedef pair<double, pair<IpRange, Cell>> Message;

class Collector {

 private:

  struct CompareCell {

    bool operator()(Message lhs, Message rhs) const {

      return lhs.first < rhs.first;

    }
  };

  static priority_queue<Message, vector<Message>, CompareCell> stats_queue;
  //mutex m;
 public:
  Collector() = default;
  void ClientHandler(int cli_fd, const char *cli_ip, int port);
  void ProcessClient(int cli_fd);
  void StartServer();
  void CleanUpStats();
  void DecodeStats(Detection::FlowStats flow_stats);
  void AggregateStats();

};

#endif //SENSS_COLLECTOR_H
