#include <fstream>
#include "util.hh"

void InitServicesSet() {
  ifstream ifs("services", ifstream::in);

  string line;
  while(ifs.good()){

    getline(ifs, line);
    if(line[0] == '#'){
      continue;
    }

    int i = line.find_first_of(" ");
    int j = line.find_first_of("#") - 1;
    while(line[i] == ' ')
      i++;
    while(line[j] == ' ')
      j--;
    service.insert(stoi(line.substr(i, j-i+1)));


  }


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

