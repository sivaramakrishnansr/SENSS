#ifndef __UTIL_HH
#define __UTIL_HH

#include <cstring>
#include <string>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <set>

#include "map.pb.h"
#include <google/protobuf/io/zero_copy_stream_impl.h>

using namespace std;

void InitServicesSet();

bool IsService(int port);

unsigned int IpToInt(const char *input);

unsigned int Min(const unsigned int &addr, const int &masklen);

unsigned int Max(const unsigned int &addr, const int &masklen);

bool readDelimitedFrom(
    google::protobuf::io::ZeroCopyInputStream *rawInput,
    google::protobuf::MessageLite *message);

bool writeDelimitedTo(
    const google::protobuf::MessageLite &message,
    google::protobuf::io::ZeroCopyOutputStream *rawOutput)

#endif
