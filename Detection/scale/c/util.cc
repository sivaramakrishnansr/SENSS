#include "util.hh"


string sha256(const string str)
{
  unsigned char hash[SHA256_DIGEST_LENGTH];
  SHA256_CTX sha256;
  SHA256_Init(&sha256);
  SHA256_Update(&sha256, str.c_str(), str.size());
  SHA256_Final(hash, &sha256);
  stringstream ss;
  for(int i = 0; i < SHA256_DIGEST_LENGTH; i++)
    {
      ss << hex << setw(2) << setfill('0') << (int)hash[i];
    }
  return ss.str();
}

int getindex(unsigned int ip, int i)
{
  stringstream ss;
  ss << ip << i;
  sha256(ss.str());
  return 3;
}

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
  int result = 0;
  int octet = 0;
  for (int i=0; i<strlen(input); i++)
    {
      if (input[i] == '.')
	{
	  result = result*256 + octet;
	  octet = 0;
	}
      else
	{
	  octet = octet*10 + input[i] - '0';
	}
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

