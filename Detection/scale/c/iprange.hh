#ifndef __IPRANGE_HH
#define __IPRANGE_HH

class iprange
{
public:
    iprange(unsigned int, unsigned int);

    /*  friend bool operator== (const iprange &i1, const iprange &i2);
        friend bool operator^ (const iprange &i1, const iprange &i2);*/
    bool contains(const iprange &i) const;

    void update(unsigned int, unsigned int);

    friend bool operator<(const iprange &i1, const iprange &i2);

    /*  friend bool operator> (const iprange &i1, const iprange &i2); */

    unsigned int min;
    unsigned int max;
};

#endif
