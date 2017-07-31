//
// Created by Abdul Qadeer on 7/19/17.
//

#include "collector.h"
#include "map.pb.h"

void Collector::StartServer() {

  int serv_fd, cli_fd, r, len;
  struct sockaddr_un local, remote;

  signal(SIGCHLD,SIG_IGN); // Reaps zombie children automatically after they are terminated
  serv_fd = socket(AF_UNIX, SOCK_STREAM, 0);
  //fcntl(serv_fd, F_SETFL, O_NONBLOCK);
  if(serv_fd < 0){
    //TODO: Use a better logging mechanism
    perror("server socket");
    return;
  }
  local.sun_family = AF_UNIX;
  strcpy(local.sun_path, "sock/server");
  unlink(local.sun_path);
  len =  sizeof(local.sun_path) + sizeof(local.sun_family);

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

  socklen_t sock_len;
  struct sockaddr_storage addr;
  char cli_ip[128];
  int port;

  sock_len = sizeof addr;
  for (;;)
  {
    cli_fd = accept(serv_fd, NULL, NULL);
    if(cli_fd > 0) {
      getpeername(serv_fd, (struct sockaddr*)&addr, &sock_len);

      if (addr.ss_family == AF_INET) {
        struct sockaddr_in *s = (struct sockaddr_in *)&addr;
        port = ntohs(s->sin_port);
        inet_ntop(AF_INET, &s->sin_addr, cli_ip, sizeof cli_ip);
      } else { // AF_INET6
        struct sockaddr_in6 *s = (struct sockaddr_in6 *)&addr;
        port = ntohs(s->sin6_port);
        inet_ntop(AF_INET6, &s->sin6_addr, cli_ip, sizeof cli_ip);
      }

      cout<<"Accepted from client  "<<cli_ip<<":"<<port<<endl;

      switch (fork()) { // Fork a new process for each reader
        case -1: // Error
          perror("server fork");
        case 0:  // Child
          while(recv(cli_fd, NULL, 0, MSG_PEEK | MSG_DONTWAIT) != 0) { // Loop until the client has closed the connection or finished processing
            ProcessClient(cli_fd);
          }
          cout<<"Disconnecting from client"<<cli_ip<<":"<<port<<endl;
          break;
        default: /* parent */
          r = close(cli_fd);
          if (r < 0) {
            perror("server close");
          }
          break;
      }
      ProcessClient(cli_fd);

    }
  }

}

void Collector::ProcessClient(int cli_fd){

  Detection::FlowStats received_stats;
  string binary_data;

  received_stats.ParseFromFileDescriptor(cli_fd);
  PopulateStats(received_stats);
}

void Collector::PopulateStats(Detection::FlowStats received_stats) {

  google::protobuf::RepeatedPtrField<Detection::FlowKeyValue> fkv_container  = received_stats.entry();
  google::protobuf::internal::RepeatedPtrIterator<Detection::FlowKeyValue> fkv_it = fkv_container.begin();

  for(; fkv_it != fkv_container.end(); fkv_it++){
    Detection::Cell received_cell = fkv_it->value();
    Cell cell;
    cell.output = received_cell.output();
    int n = received_cell.cols();
    for(int i = 0; i < received_cell.bytes_size(); i++){
      cell.bytes[i/n][i%n] = received_cell.bytes(i);
      cell.pkts[i/n][i%n] = received_cell.pkts(i);
    }

    IpRange ip_range(fkv_it->key().min(), fkv_it->key().max());
    if(stats[ip_range].find(received_stats.time()) == stats[ip_range].end()){
      stats[ip_range][received_stats.time()].reserve(kReaderCount);
    }
    stats[ip_range][received_stats.time()].push_back(cell);
  }

}

