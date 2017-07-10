#ifndef __FLOW_HH
#define __FLOW_HH


class flow
{
public:
  flow();
  flow(double, double, unsigned int, unsigned int, int, int, int, int);
  void init(double, double, unsigned int, unsigned int, int, int, int, int);

  unsigned int saddr, daddr;
  double first, last;
  int pkts, bytes, proto, flags;
};
  

#endif
