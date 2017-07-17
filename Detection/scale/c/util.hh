#ifndef __UTIL_HH
#define __UTIL_HH

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <openssl/sha.h>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>

using namespace std;

string sha256(const string str);
int getindex(unsigned int, int);
bool isservice(int port);
unsigned int ip2int(const char* input);
unsigned int min(const unsigned int & addr, const int & masklen);
unsigned int max(const unsigned int & addr, const int & masklen);

#endif
