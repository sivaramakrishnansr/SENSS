#include "flow.hh"


flow::flow(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl) {
  init(p, b, f, l, s, d, sp, dp, pr, fl);
};

void flow::init(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl) {
  pkts = p;
  bytes = b;
  first = f;
  last = l;
  saddr = s;
  daddr = d;
  sport = sp;
  dport = dp;
  proto = pr;
  flags = fl;
};


