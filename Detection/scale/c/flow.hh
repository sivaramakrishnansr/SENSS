#ifndef __FLOW_HH
#define __FLOW_HH

class Flow {
 public:
  Flow() = default;
  Flow(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl);

  void Init(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl);

  unsigned int saddr = 0, daddr = 0;
  double first, last;
  int sport, dport, pkts, bytes, proto, flags;
};

#endif
