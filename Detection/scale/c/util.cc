#include <fstream>
#include "util.hh"

void init(int port) {
  // TODO: this needs to be more comprehensive. Should read
  // ports from services.txt

  if (port == 80 || port == 53 || port == 443 || port == 22) {
    return true;
  }
  return false;
}

unsigned int ip2int(const char *input) {
  int result = 0;
  int octet = 0;
  for (int i = 0; i < strlen(input); i++) {
    if (input[i] == '.') {
      result = result * 256 + octet;
      octet = 0;
    } else {
      octet = octet * 10 + input[i] - '0';
    }
  }
  return result;
}

unsigned int min(const unsigned int &addr, const int &masklen) {
  return addr & (~0 << (32 - masklen));
}

unsigned int max(const unsigned int &addr, const int &masklen) {
  int toor = (1 << (32 - masklen)) - 1;
  return (addr & (~0 << (32 - masklen))) | toor;
}

