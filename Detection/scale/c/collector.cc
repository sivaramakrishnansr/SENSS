//
// Created by Abdul Qadeer on 7/19/17.
//

#include "collector.h"
#include "map.pb.h"

void Collector::StartServer() {

  int serv_fd, cli_fd, r, len;
  struct sockaddr_un local, remote;

  serv_fd = socket(AF_UNIX, SOCK_STREAM, 0);
  if(serv_fd < 0){
    //TODO: Use a better logging mechanism
    perror("server socket");
    return;
  }
  local.sun_family = AF_UNIX;
  strcpy(local.sun_path, "sock/server");
  unlink(local.sun_path);
  len =  strlen(local.sun_path) + sizeof(local.sun_family);

  r = ::bind(serv_fd, (struct sockaddr *)&local, len);
  if(r < 0){
    perror("server bind");
    return;
  }

  r = listen(serv_fd, 100);
  if(r < 0){
    perror("server listen");
    return;
  }

  for (;;)
  {
    cli_fd = accept(serv_fd, NULL, NULL);
    if (cli_fd < 0)
      perror("server accept");
    switch (fork())
    {
      case -1: /* error */
        perror("server fork");
      case 0:  /* child */
        ProcessClient(cli_fd);
        close(serv_fd);
        return;
      default: /* parent */
        r = close(cli_fd);
        if(r < 0){
          perror("server close");
        }
        break;
    }
  }

}

void Collector::ProcessClient(int cli_fd){

  size_t i = 0;
  char buf[8096];
  size_t r;
  Detection::FlowStats stats;
  string binary_data;

//  while((r = read(cli_fd, buf, 1)) > 0){
//    binary_data.append(buf, r);
//  }
  stats.ParseFromFileDescriptor(cli_fd);
  for(auto i : stats.entries()){
    cout<<i.key().min();
  }

}

