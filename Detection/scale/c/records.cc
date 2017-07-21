
#include "records.h"
#include "map.pb.h"
#include "util.h"


void FlowRecord::Update(const Flow &f, int dstours, int recordours) {
  double ps = (f.last - f.first) / kPeriod + 1;
  double pkts = f.pkts / ps;
  double bytes = f.bytes / ps;
  int issrc;
  int isreq;
  if (f.proto == 6) {
    // TCP conns w push get to be counted as successful
    if (f.flags & 8)
      isreq = 0;
    else
      isreq = 1;
  } else if (IsService(f.sport) && !IsService(f.dport))
    isreq = 0;
  else if (!IsService(f.sport) && IsService(f.dport))
    isreq = 1;
  else {
    // Regard all other traffic as requests
    isreq = 1;
  }
  if (dstours) {
    // Our destination
    IpRange srange(Min(f.saddr, kForeignMask), Max(f.saddr, kForeignMask));
    IpRange drange(Min(f.daddr, kHomeMask), Max(f.daddr, kHomeMask));
    if (recordours) {
      // Our destination, our records, reply pkt
      issrc = 0;
      for (int i = 0; i < kBinCount; i++) {
        stats[drange].Add(issrc, isreq, pkts, bytes);
      }
    } else {
      // Our destination, foreign records, reply pkt
      issrc = 1;
      stats[srange].Add(issrc, isreq, pkts, bytes);
    }
  } else {
    // Our source
    IpRange srange(Min(f.saddr, kHomeMask), Max(f.saddr, kHomeMask));
    IpRange drange(Min(f.daddr, kForeignMask), Max(f.daddr, kForeignMask));
    if (recordours) {
      // Our source, our records
      issrc = 1;
      stats[srange].Add(issrc, isreq, pkts, bytes);
    } else {
      // Our source, foreign records
      issrc = 0;
      stats[drange].Add(issrc, isreq, pkts, bytes);
    }
  }
}

int FlowRecord::Size() {
  return 1; //stats.size();
}

void FlowRecord::Report(double time) {
  /* TODO: this is just for testing, but instead
     we should read all the records and send over the net
     to the collector */
  unsigned int add = IpToInt("207.75.112.0");
  IpRange range(Min(add, 24), Max(add, 24));
  if (stats.find(range) != stats.end()) {
    string co = stats[range].ToString();
    printf("%lf For 207.75.112.0 stats are %s\n", time, co.c_str());
  }
  // This should stay
  stats.clear();
}
