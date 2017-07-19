#include <fstream>
#include "util.hh"

set<int> service;

void InitServicesSet() {
  ifstream ifs("services", ifstream::in);
  string line;
  while(ifs.good()){
    getline(ifs, line);
    //Skip if the line begins with # i.e. a comment
    if(line[0] == '#'){
      continue;
    }
    stringstream ss(line);
    while(getline(ss, line, '\t')){
      if((isdigit(line[0])) && (line.find("udp") != string::npos || line.find("tcp") != string::npos)){
        service.insert(stoi(line));
        break;
      }
    }
  }

}

bool IsService(int port){
  if(service.find(port) != service.end())
    return true;
  return false;
}

unsigned int IpToInt(const char *input) {
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

unsigned int Min(const unsigned int &addr, const int &masklen) {
  return addr & (~0 << (32 - masklen));
}

unsigned int Max(const unsigned int &addr, const int &masklen) {
  int toor = (1 << (32 - masklen)) - 1;
  return (addr & (~0 << (32 - masklen))) | toor;
}

