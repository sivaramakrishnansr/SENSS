#include "records.hh"

records::records()
{
} 

void records::insert(iprange ip, int i, int j, int p, int b)
{
  stats[ip].insert(i, j, p, b);
}




