#ifndef __UTIL_HH
#define __UTIL_HH

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <set>

using namespace std;

int getindex(unsigned int, int);

void InitServicesSet();

unsigned int ip2int(const char *input);

unsigned int min(const unsigned int &addr, const int &masklen);

unsigned int max(const unsigned int &addr, const int &masklen);

set<int> service;

#endif
