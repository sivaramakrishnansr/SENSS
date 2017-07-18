#include "records.hh"
#include "util.hh"


records::records()
{
  stats = new cell*[BINCOUNT];
  for (int i=0;i<BINCOUNT;i++)
    stats[i] = new cell[BINSIZE];
} 

void records::update(const flow &f, int dstours, int recordours)
{
  double ps = (f.last-f.first)/PERIOD+1;
  double pkts = f.pkts/ps;
  double bytes = f.bytes/ps;
  int issrc;
  int isreq;
  if (f.proto == 6)
    {
      // TCP conns w push get to be counted as successful
      if (f.flags & 16)
	isreq = 0;
      else
	isreq = 1;
    }
  else if (isservice(f.sport) && !isservice(f.dport))
    isreq = 0;
  else if(!isservice(f.sport) && isservice(f.dport))
    isreq = 1;
  else
    {
    // Regard all other traffic as requests
      isreq = 1;
    }
  if (dstours)
    {
      // Our destination
      unsigned int src = min(f.saddr,foreign_mask);
      unsigned int dst = min(f.daddr,home_mask);
      int indexes[2][BINCOUNT];
      for (int i=0; i<BINCOUNT;i++)
	{
	  indexes[0][i] = getindex(src,i);
	  indexes[1][i] = getindex(dst,i);
	}
      
      if (recordours)
	{
	  // Our destination, our records, reply pkt	      
	  issrc = 0;
	  for (int i=0; i<BINCOUNT;i++)
	    {
	      stats[i][indexes[1][i]].add(issrc, isreq, pkts, bytes);
	    }
	}
      else
	{
	  // Our destination, foreign records, reply pkt
	  issrc = 1;
	  //stats[srange].add(issrc, isreq, pkts, bytes);
	}
    }
  else
    {
      // Our source
      iprange srange(min(f.saddr,home_mask), max(f.saddr,home_mask));
      iprange drange(min(f.daddr,foreign_mask), max(f.daddr,foreign_mask));

      if (recordours)
	{
	  // Our source, our records
	      issrc = 1;
	      //stats[srange].add(issrc, isreq, pkts, bytes);
	}
      else
	{
	  // Our source, foreign records
	  issrc = 0;
	  //stats[drange].add(issrc, isreq, pkts, bytes);
	}
    }
}

int records::size()
{
  return 1; //stats.size();
}

void records::report(double time)
{
  /* TODO: this is just for testing, but instead
     we should read all the records and send over the net
     to the collector */
  unsigned int add = ip2int("207.75.112.0");
  iprange range(min(add,24), max(add,24));
  if (stats.find(range) != stats.end())
    {
      const char* co = stats[range].tostr();
      printf("%lf For 207.75.112.0 stats are %s\n", time, co);
    }
  // This should stay
  stats.clear();
}
