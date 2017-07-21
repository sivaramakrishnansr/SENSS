#ifndef __UTIL_HH
#define __UTIL_HH

#include <cstring>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <set>

using namespace std;

void InitServicesSet();

bool IsService(int port);

unsigned int IpToInt(const char *input);

unsigned int Min(const unsigned int &addr, const int &masklen);

unsigned int Max(const unsigned int &addr, const int &masklen);



#endif
