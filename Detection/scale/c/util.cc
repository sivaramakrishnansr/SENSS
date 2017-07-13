#include "util.hh"

bool isservice(int port)
{
  // TODO: this needs to be more comprehensive
  if (port == 80 || port == 53 || port == 443 || port == 22)
    {
      return true;
    }
  return false;
}

unsigned int ip2int(const char* input)
{
  char ip[17];
  strncpy(ip, input, strlen(input));
  char* word = strtok(ip, ".");
  int result=atoi(word);
  while ((word = strtok(NULL, ".")) != NULL)
    {
      result = result*256+atoi(word);
    }
  return result;
}

unsigned int min(const unsigned int & addr, const int & masklen)
{
  return addr & (~0 << (32-masklen));
}

unsigned int max(const unsigned int & addr, const int & masklen)
{
  int toor = (1 << (32-masklen))-1;
  return (addr & (~0 << (32-masklen))) | toor;
}

