#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <iostream>
#include <fstream>
#include <map>
#include <math.h>
#include <thread>
#include <unistd.h>
#include "boost/filesystem.hpp"
#include "reader.h"
#include "records.h"
#include "util.h"
#include "collector.h"

using namespace std;


const int CHUNK = 10;

Flow flows[CHUNK];
int numflows = 0;
FlowRecord home, foreign;
map<double, int> times;
int Reader::clifd = 0;

int ours = 0, ourd = 0, neither = 0, both = 0;
double curT = 0, prevT = 0;

/* Process by double-buffering because of reordering.
This way we can find the most frequent time and only
process flows related to it */

void Reader::ProcessFlowHelper(Flow f) {
  int mask = 32;
  IpRange srange(Min(f.saddr, mask), Max(f.saddr, mask));
  IpRange drange(Min(f.daddr, mask), Max(f.daddr, mask));

  map<IpRange, int>::iterator sit = blocks.find(srange);
  map<IpRange, int>::iterator dit = blocks.find(drange);
  if (sit == blocks.end() && dit != blocks.end()) {
    ourd++;
    // Destination is ours, records may or may not be
    home.Update(f,1,1);
    foreign.Update(f,1,0);
  } else if (sit != blocks.end() && dit == blocks.end()) {
    ours++;
    // Source is ours, records may or may not be
    home.Update(f,0,1);
    foreign.Update(f,0,0);
  } else if (sit == blocks.end() && dit == blocks.end())
    neither++;
  else
    both++;
}

void Reader::Report(double time) {

//  cout.precision(15);
//  cout << fixed << time << endl;
  home.Report(time, clifd);
  //foreign.Report(time, clifd);
}

void Reader::ProcessFlow() {
  int max = 0;
  double maxT = 0;

  for (map<double, int>::iterator it = times.begin(); it != times.end(); it++) {
    if (times[it->first] > max) {
      max = times[it->first];
      maxT = it->first;
    }
  }
  prevT = curT;
  if (maxT > curT) {
    curT = maxT;
    //printf("CurT %lf home %d foreign %d\n", curT, home.Size(), foreign.Size());
  }
  times.clear();
  // See which flows we can fully process and which we have to keep
  int start = 0;
  for (int i = 0; i < numflows; i++) {
    // Ignore, drop
    if (flows[i].first < prevT && flows[i].last < prevT) {
    }
      // Fully process, this is the last second
    else if ((flows[i].first <= curT && flows[i].last <= curT) ||
        (flows[i].first <= prevT && flows[i].last <= prevT)) {
      ProcessFlowHelper(flows[i]);
    }
      // Partially process, drop to save space
    else if ((flows[i].first <= curT && flows[i].last > curT) ||
        (flows[i].first <= prevT && flows[i].last > prevT)) {
      //TODO: should really keep for at least a while
      ProcessFlowHelper(flows[i]);
      //flows[start++] = flows[i];
    }
      // Don't process, keep
    else if (flows[i].first > curT && flows[i].last > curT) {
      flows[start++] = flows[i];
    }
  }
  numflows = start;
  // Time to report
  if (prevT < curT) {
    Report(prevT);
  }
}

void Reader::ReadFlow(char *buffer) {

  int sport = 0, dport = 0, prot = 0, flags = 0, pkts = 0, bytes = 0, i = 0;
  double first = 0, last = 0;
  char *p = strtok(buffer, ",");
  char *field[10];
  while (p) {
    field[i++] = p;
    p = strtok(NULL, ",");
  }

  // Work with first and last, rounded down using period
  first = floor(atof(field[2]) / kPeriod * 100) / 100;
  last = floor(atof(field[3]) / kPeriod * 100) / 100;
  unsigned int saddr = IpToInt(field[4]);
  unsigned int daddr = IpToInt(field[5]);
  times[first]++;
  times[last]++;

  pkts = atoi(field[0]);
  bytes = atoi(field[1]);
  first = strtod(field[2], NULL);
  last = strtod(field[3], NULL);
  sport = atoi(field[6]);
  dport = atoi(field[7]);
  prot = atoi(field[8]);
  flags = atoi(field[9]);

  flows[numflows++].Init(pkts, bytes, first, last, saddr, daddr, sport, dport, prot, flags);

  if (numflows == CHUNK) {
    ProcessFlow();
  }
}

void Reader::LoadBlocks() {
  string buffer;
  ifstream blockfile;
  blockfile.open("blocks", ios::in);

  while (getline(blockfile, buffer)) {
    char ip[17];
    int mask;
    int pos = buffer.find("/");
    strncpy(ip, buffer.c_str(), pos);
    ip[pos] = 0;
    mask = atoi(buffer.c_str() + pos + 1);
    unsigned int add = IpToInt(ip);
    IpRange range(Min(add, mask), Max(add, mask));
    map<IpRange, int>::iterator it = blocks.find(range);

    // Check if what we found is a smaller range and should be replaced
    if (it != blocks.end()) {
      if (range.Contains(it->first)) {
        blocks.erase(it->first);
        blocks[range] = 1;
      }
    } else {
      blocks[range] = 1;
    }
  }
}
// Connect the client to the server whose address is specified by servaddr
void Reader::ConnectClient(const char * servaddr){

  int r, len;
  struct sockaddr_un remote;
  remote.sun_family = AF_UNIX;
  strcpy(remote.sun_path, kServerAddress);
  len = sizeof(remote.sun_path) + sizeof(remote.sun_family);

  clifd = socket(AF_UNIX, SOCK_STREAM, 0);
  if(clifd < 0) {
    perror("client socket");
  }

  r = connect(clifd, (struct sockaddr *)&remote, len);

  if(r < 0){
    perror("client connect");
  }

}

int main() {
  // Read in blocks
  Collector collector;
  thread t(bind(&Collector::StartServer, collector));
  //thread t2(bind(&Collector::AggregateStats, collector));
  //collector.StartServer();
  Reader reader;
  reader.LoadBlocks();
  reader.ConnectClient(kServerAddress);
  // Initialise services set
  InitServicesSet();


  // Print them out just for kicks

//  for (map<IpRange, int>::iterator it = blocks.begin(); it != blocks.end(); ++it) {
//    printf("Block %u %u\n", it->first.min, it->first.max);
//  }

  // Verify that the version of the library that we linked against is
  // compatible with the version of  the headers we compiled against.
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  char buffer[256];
  FILE * fp = fopen("data/test", "r");
  while (fgets(buffer, 255, fp)) {
    if(buffer[0] == '#') // Skips comments
      continue;
    reader.ReadFlow(buffer);
  }
  printf("Ours %d ourd %d neither %d both %d\n", ours, ourd, neither, both);
  close(Reader::clifd);
  // Delete all global objects allocated by libprotobuf.
  google::protobuf::ShutdownProtobufLibrary();
  //t.join();
//  t2.join();
}

