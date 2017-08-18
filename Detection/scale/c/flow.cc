#include "flow.h"

Flow::Flow(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl) {
  Init(p, b, f, l, s, d, sp, dp, pr, fl);
};

void Flow::Init(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl) {
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


