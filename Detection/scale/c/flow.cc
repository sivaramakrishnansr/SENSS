#include "flow.hh"

flow::flow()
{
  saddr = daddr = 0;
}

flow::flow(double f, double l, unsigned int s, unsigned int d, int sp, int dp, int p, int b, int pr, int fl)
{
  init(f, l, s, d, sp, dp, p, b, pr, fl);
};

void flow::init(double f, double l, unsigned int s, unsigned int d, int sp, int dp, int p, int b, int pr, int fl)
{
  first = f;
  last = l;
  saddr = s;
  daddr = d;
  sport = sp;
  dport = dp;
  pkts = p;
  bytes = b;
  proto = pr;
  flags = fl;
};


