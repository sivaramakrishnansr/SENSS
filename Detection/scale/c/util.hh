#ifndef __UTIL_HH
#define __UTIL_HH

#include <string.h>
#include <stdlib.h>

bool isservice(int port);
unsigned int ip2int(const char* input);
unsigned int min(const unsigned int & addr, const int & masklen);
unsigned int max(const unsigned int & addr, const int & masklen);

#endif
