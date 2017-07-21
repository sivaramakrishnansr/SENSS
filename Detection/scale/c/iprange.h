#ifndef __IPRANGE_HH
#define __IPRANGE_HH

class IpRange {
 public:
  IpRange(unsigned int, unsigned int);

  /*  friend bool operator== (const iprange &i1, const iprange &i2);
      friend bool operator^ (const iprange &i1, const iprange &i2);*/
  bool Contains(const IpRange &i) const;

  void Update(unsigned int, unsigned int);

  friend bool operator<(const IpRange &i1, const IpRange &i2);

  /*  friend bool operator> (const iprange &i1, const iprange &i2); */

  unsigned int min;
  unsigned int max;
};

#endif
