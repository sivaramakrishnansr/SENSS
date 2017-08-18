//
// Created by Abdul Qadeer on 7/19/17.
//

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <arpa/inet.h>
#include <iostream>
#include <unistd.h>
#include <queue>
#include <thread>

#include "cell.h"
#include "config.h"
#include "collector.h"
#include "util.h"

#include <google/protobuf/io/zero_copy_stream_impl.h>

#define mp make_pair

priority_queue<Message, vector<Message>, Collector::CompareCell>  Collector::stats_queue;

void Collector::ClientHandler(int cli_fd, const char *cli_ip, int port) {

  cout << "Connection from client  " << cli_ip << ":" << port << endl;

  while (true) {
    ProcessClient(cli_fd);
  }
  /*
   * TODO: Need a way to check if the client has finished sending data, in which case the following code executes.
   * recv sys call with appropriate flags (recv(cli_fd, NULL, 0, MSG_PEEK | MSG_DONTWAIT)) won't work because it returns 0
   * as soon as the client is done with a batch of messages. One possible way is to send a special message from client
   */
  cout << "Disconnecting from client" << cli_ip << ":" << port << endl;
  close(cli_fd);
}

void Collector::StartServer() {

  int serv_fd, cli_fd, r, len;
  struct sockaddr_un local, remote;

  signal(SIGCHLD, SIG_IGN); // Reaps zombie children automatically after they are terminated
  serv_fd = socket(AF_UNIX, SOCK_STREAM, 0);

  if (serv_fd < 0) {
    //TODO: Use a better logging mechanism
    perror("server socket");
    return;
  }
  local.sun_family = AF_UNIX;
  strcpy(local.sun_path, "sock/server");
  unlink(local.sun_path);
  len = sizeof(local.sun_path) + sizeof(local.sun_family);

  r = ::bind(serv_fd, (struct sockaddr *) &local, len);

  if (r < 0) {
    perror("server bind");
    return;
  }

  r = listen(serv_fd, 100);
  if (r < 0) {
    perror("server listen");
    return;
  }

  socklen_t sock_len;
  struct sockaddr_storage addr;
  char cli_ip[128];
  int port;

  sock_len = sizeof addr;
  thread *t;
  for (;;) {
    cli_fd = accept(serv_fd, NULL, NULL);

    if (cli_fd > 0) {
      getpeername(serv_fd, (struct sockaddr *) &addr, &sock_len);

      if (addr.ss_family == AF_INET) {
        struct sockaddr_in *s = (struct sockaddr_in *) &addr;
        port = ntohs(s->sin_port);
        inet_ntop(AF_INET, &s->sin_addr, cli_ip, sizeof cli_ip);
      } else if (addr.ss_family == AF_INET6) { // AF_INET6
        struct sockaddr_in6 *s = (struct sockaddr_in6 *) &addr;
        port = ntohs(s->sin6_port);
        inet_ntop(AF_INET6, &s->sin6_addr, cli_ip, sizeof cli_ip);
      } else if (addr.ss_family == AF_UNIX) {
        struct sockaddr *s = (struct sockaddr *) &addr;
        strncpy(cli_ip, s->sa_data, sizeof s->sa_data);
      }
      t = new thread(&Collector::ClientHandler, this, cli_fd, cli_ip, port);

    } else {
      perror("server accept");
      return;
    }
  }

}

/*
 * Read protobuf messages from the socket open
 */

void Collector::ProcessClient(int cli_fd) {

  Detection::FlowStats received_stats;
  string binary_data;

  google::protobuf::io::ZeroCopyInputStream *rawInput = new google::protobuf::io::FileInputStream(cli_fd);
  google::protobuf::MessageLite *message = &received_stats;

  if (readDelimitedFrom(rawInput, message))
    DecodeStats(received_stats);
  delete rawInput;
}

/*
 * Decodes the protobuf message and fills in the stats_queue with it
 */

void Collector::DecodeStats(Detection::FlowStats received_stats) {

  google::protobuf::RepeatedPtrField<Detection::FlowKeyValue> fkv_container = received_stats.entry();
  google::protobuf::internal::RepeatedPtrIterator<Detection::FlowKeyValue> fkv_it = fkv_container.begin();

  for (; fkv_it != fkv_container.end(); fkv_it++) {
    Detection::Cell received_cell = fkv_it->value();
    Cell cell;
    cell.output = received_cell.output();
    int n = received_cell.cols();
    for (int i = 0; i < received_cell.bytes_size(); i++) {
      cell.bytes[i / n][i % n] = received_cell.bytes(i);
      cell.pkts[i / n][i % n] = received_cell.pkts(i);
    }

    IpRange ip_range(fkv_it->key().min(), fkv_it->key().max());
    stats_queue.push(mp(received_stats.time(), mp(ip_range, cell)));
  }

}

/*
 * Remove all messages from queue every 5 seconds and extract any features from them
 */
void Collector::AggregateStats() {

  static int cnt = 0;

  while (true) {
    sleep(5);
    if (stats_queue.empty())
      continue;
    cout << "Processing batch " << cnt++ << "   " << stats_queue.size() << endl;
    //double start = stats_queue.top().first;
    vector<Message> to_process;
    to_process.reserve(kReaderCount);
    while (!stats_queue.empty()) {
      Message msg = stats_queue.top();
      stats_queue.pop();
      cout.precision(15);
      cout << fixed << msg.first << endl;
    }
  }

  //TODO: Process the aggregated Messages in vector to_process - extract features etc.

}

int main() {

  Collector collector;
  cout << "Starting collector server" << endl;
  thread t(bind(&Collector::AggregateStats, collector));
  collector.StartServer();
}