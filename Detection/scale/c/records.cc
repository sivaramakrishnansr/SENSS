#include "records.hh"
#include "util.hh"

#include <stdio.h>

records::records()
{
} 

void records::update(const flow &f, int dstours, int recordours)
{
  double ps = (f.last-f.first)/PERIOD+1;
  double pkts = f.pkts/ps;
  double bytes = f.pkts/ps;
  int issrc;
  int isreq;
  if (dstours)
    {
      iprange srange(min(f.saddr,foreign_mask), max(f.saddr,foreign_mask));
      iprange drange(min(f.daddr,home_mask), max(f.daddr,home_mask));
      if (isservice(f.sport) && !isservice(f.dport))
	{
	  if (recordours)
	    {
	      isreq = 0;
	      issrc = 0;
	    }
	  else
	    {
	      isreq = 0;
	      issrc = 1;
	    }
	    stats[drange].add(issrc, isreq, pkts, bytes);
	}
      else if (!isservice(f.sport) && isservice(f.dport))
	{
	  if (recordours)
	    {
	      isreq = 1;
	      issrc = 0;
	    }
	  else
	    {
	      isreq = 1;
	      issrc = 1;
	    }
	  stats[drange].add(issrc, isreq, pkts, bytes);
	}
    }
  else // !dstours
    {
      iprange srange(min(f.saddr,home_mask), max(f.saddr,home_mask));
      iprange drange(min(f.daddr,foreign_mask), max(f.daddr,foreign_mask));

      if (isservice(f.sport) && !isservice(f.dport))
	{
	  if (recordours)
	    {
	      isreq = 0;
	      issrc = 1;
	    }
	  else
	    {
	      isreq = 0;
	      issrc = 0;
	    }
	    stats[srange].add(issrc, isreq, pkts, bytes);
	}
      else if (!isservice(f.sport) && isservice(f.dport))
	{
	  if (recordours)
	    {
	      isreq = 1;
	      issrc = 1;
	    }
	  else
	    {
	      isreq = 1;
	      issrc = 0;
	    }
	    stats[srange].add(issrc, isreq, pkts, bytes);
	}
    }
}

int records::size()
{
  return stats.size();
}

