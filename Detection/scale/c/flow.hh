#ifndef __FLOW_HH
#define __FLOW_HH

#include "util.hh"

class flow
{
public:
    flow();

    flow(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl);

    void init(int p, int b, double f, double l, unsigned int s, unsigned int d, int sp, int dp, int pr, int fl);

    unsigned int saddr, daddr;
    double first, last;
    int sport, dport, pkts, bytes, proto, flags;
};


#endif
