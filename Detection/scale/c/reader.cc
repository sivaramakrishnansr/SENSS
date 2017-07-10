#include <iostream>
#include <fstream>
#include <map>

#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "iprange.hh"
#include "records.hh"
#include "flow.hh"

using namespace std;
map<iprange,int> blocks;
double PERIOD=1;
const int CHUNK=1000;
int FOREIGN=0;
int HOME=1;

flow flows[CHUNK];
int numflows=0;

records home, foreign;
map<double, int> times;

unsigned int ip2int(const char* input)
{
  char ip[17];
  strncpy(ip, input, strlen(input));
  char* word = strtok(ip, ".");
  int result=atoi(word);
  while ((word = strtok(NULL, ".")) != NULL)
    {
      result = result*256+atoi(word);
    }
  return result;
}

unsigned int min(unsigned int addr, int masklen)
{
  return addr & (~0 << (32-masklen));
}

unsigned int max(unsigned int addr, int masklen)
{
  int toor = (1 << (32-masklen))-1;
  return (addr & (~0 << (32-masklen))) | toor;
}

int ours=0, ourd=0, neither=0, both=0;
int processed=0;

/* Process by double-buffering because of reordering. 
This way we can find the most frequent time and only
process flows related to it */

void reprocess()
{

  int max = 0;
  double maxT = 0;
  for (map<double,int>::iterator it = times.begin(); it != times.end(); it++)
    {
      if (times[it->first] > max)
	{
	  max = times[it->first];
	  maxT = it->first;
	}
    }
  printf("Max %d maxT %lf\n", max, maxT);
  
  for (int i=0; i<numflows; i++)
    {
      /*
      int mask = 32;
      // Use different masks for home and foreign
      iprange srange(min(flows[i].saddr,mask), max(flows[i].saddr,mask));
      iprange drange(min(flows[i].daddr,mask), max(flows[i].daddr,mask));
      
      map<iprange,int>::iterator sit = blocks.find(srange);
      map<iprange,int>::iterator dit = blocks.find(drange);
      if (sit == blocks.end() && dit != blocks.end())
	{
	  // TODO: Change this so it's variable mask for foreign and home
	  ourd++;
	  //store(FOREIGN, srange, 0, 0, pkts, bytes, first, last);
	  //foreign.insert(srange,0,0,pkts,bytes);
	}
      else if (sit != blocks.end() && dit == blocks.end())
	{
	  ours++;
	  //store(HOME, srange, 0, 0, pkts, bytes, first, last);
	  // TODO: Change this so it's variable mask for foreign and home
	  //home.insert(srange,0,0,pkts,bytes);
	}
      else if (sit == blocks.end() && dit == blocks.end())
	neither++;
      else
	both++;
      */
    }
  numflows = 0;
}



void process(char* buffer)
{
  char src[17], dst[17];
  int sport, dport, proto, flags, pkts, bytes;
  double first, last;
  char* word = strtok(buffer, ",");
  int i=0;
  while ((word = strtok(NULL, ",")) != NULL)
	{
	  i++;
	  switch(i)
	    {
	    case 4:
	      pkts=atoi(word);
	      break;
	    case 5:
	      bytes=atoi(word);
	      break;
	    case 6:
	      first = strtod(word,NULL);
	      break;
	    case 7:
	      last = strtod(word,NULL);
	      break;
	    case 10:
	      strncpy(src,word,strlen(word));
	      break;
	    case 11:
	      strncpy(dst,word,strlen(word));
	      break;
	    case 14:
	      sport=atoi(word);
	      break;
	    case 15:
	      dport=atoi(word);
	      break;
	    case 16:
	      proto=atoi(word);
	      break;
	    case 18:
	      flags=atoi(word);
	      break;
	    default:
	      break;
	    }
	}
  // Work with first and last, rounded down using period
  first = floor(first/PERIOD*100)/100;
  last = floor(last/PERIOD*100)/100;
  unsigned int saddr = ip2int(src);
  unsigned int daddr = ip2int(dst);
  times[first]++;
  times[last]++;
  
  flows[numflows++].init(first, last, saddr, daddr, pkts, bytes, proto, flags);

  if (numflows == CHUNK)
    {
      reprocess();
    }
}


void loadblocks()
{
  string buffer;
  ifstream blockfile;
  blockfile.open("blocks",ios::in);
  while (getline(blockfile,buffer))
    {
      char copy[255];
      char ip[17];
      int mask;
      int pos=buffer.find("/");
      strncpy(ip,buffer.c_str(),pos);
      ip[pos]=0;
      mask=atoi(buffer.c_str()+pos+1);
      unsigned int add=ip2int(ip);
      iprange range(min(add,mask), max(add,mask));
      map<iprange,int>::iterator it = blocks.find(range);
      
      // Check if what we found is a smaller range and should be replaced
      if (it != blocks.end())
	{
	  if (range.contains(it->first))
	    {
	      blocks.erase(it->first);
	      blocks[range] = 1;
	    }
	}
      else
	{
	  blocks[range]=1;
	}
    }

}


int main()
{
  // Read in blocks
  loadblocks();

  // Print them out just for kicks
  for (map<iprange,int>::iterator it=blocks.begin(); it!=blocks.end(); ++it)
    {
      printf("Block %u %u\n", it->first.min, it->first.max);
    }
  
  char buffer[256];
  while(fgets(buffer, 255,stdin))
    {
      process(buffer);
    }
  printf("Ours %d ourd %d neither %d both %d\n", ours, ourd, neither, both);
}

