#include "iprange.hh"

IpRange::IpRange(unsigned int a, unsigned int b) {
  min = a;
  max = b;
}

void IpRange::Update(unsigned int a, unsigned int b) {
  min = a;
  max = b;
}

/*
bool operator== (const iprange &i1, const iprange &i2)
{
  return (i1.min == i2.min && i1.max == i2.max); // | (i1^i2);
}

bool operator^ (const iprange &i1, const iprange &i2)
{
  return (i1.min <= i2.Min && i1.max >= i2.max);
}
*/
bool IpRange::Contains(const IpRange &i) const {
  return (min <= i.min && max >= i.max);
}

bool operator<(const IpRange &i1, const IpRange &i2) {
  return (i1.max < i2.min) && (!i1.Contains(i2));
}

/*
bool operator> (const iprange &i1, const iprange &i2)
{
  return (i1.Min < i2.max);
}
*/
