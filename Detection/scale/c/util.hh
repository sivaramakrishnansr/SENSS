#ifndef __UTIL_HH
#define __UTIL_HH

#include <cstring>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <set>

using namespace std;

int getindex(unsigned int, int);

void InitServicesSet();

bool IsService(int port);

unsigned int ip2int(const char *input);

unsigned int min(const unsigned int &addr, const int &masklen);

unsigned int max(const unsigned int &addr, const int &masklen);



#endif
