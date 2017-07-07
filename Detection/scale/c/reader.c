#include <stdio.h>
#include <string.h>

void process(char* buffer)
{
  char src[17], dst[17];
  int sport, dport, proto, flags, pkts, bytes;
  double first, last;
  char* word = strtok(buffer, ",");
  int i=0;
  while ((word = strtok(NULL, ",")) != NULL)
	{
	  i++;
	  switch(i)
	    {
	    case 4:
	      pkts=atoi(word);
	      break;
	    case 5:
	      bytes=atoi(word);
	      break;
	    case 6:
	      first = strtod(word,NULL);
	      break;
	    case 7:
	      last = strtod(word,NULL);
	      break;
	    case 10:
	      strncpy(src,word,17);
	      break;
	    case 11:
	      strncpy(dst,word,17);
	      break;
	    case 14:
	      sport=atoi(word);
	      break;
	    case 15:
	      dport=atoi(word);
	      break;
	    case 16:
	      proto=atoi(word);
	      break;
	    case 18:
	      flags=atoi(word);
	      break;
	    default:
	      break;
	    }
	}
}

void loadblocks()
{
  char buffer[256];
  FILE* blockfile;
  blockfile=fopen("blocks","r");
  printf("file %d\n", (int)blockfile);
  while(fgets(buffer, 255,blockfile))
    {      
      char ip[17];
      int mask;
      char* word = strtok(buffer, "/");
      strncpy(ip,word,16);
      word = strtok(NULL, "\n");
      mask=atoi(word);
      printf("ip=%s mask=%d\n", ip, mask);
    }

}

int main()
{
  // Read in blocks
  loadblocks();
  char buffer[256];
  while(fgets(buffer, 255,stdin))
    {
      process(buffer);
    }
}

