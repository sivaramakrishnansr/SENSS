#include "iprange.hh"

iprange::iprange(unsigned int a, unsigned int b)
{
  min=a;
  max=b;
}

void iprange::update(unsigned int a, unsigned int b)
{
  min=a;
  max=b;
}
/*
bool operator== (const iprange &i1, const iprange &i2)
{
  return (i1.min == i2.min && i1.max == i2.max); // | (i1^i2);
}

bool operator^ (const iprange &i1, const iprange &i2)
{
  return (i1.min <= i2.min && i1.max >= i2.max);
}
*/
bool iprange::contains(const iprange &i) const
{
  return (min <= i.min && max >= i.max);
}

bool operator< (const iprange &i1, const iprange &i2)
{
  return (i1.max < i2.min) && (!i1.contains(i2));
}

/*
bool operator> (const iprange &i1, const iprange &i2)
{
  return (i1.min < i2.max);
}
*/
