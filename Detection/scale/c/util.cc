#include <fstream>
#include "util.h"


set<int> service;

void InitServicesSet() {
  ifstream ifs("services", ifstream::in);
  string line;
  while (ifs.good()) {
    getline(ifs, line);
    //Skip if the line begins with # i.e. a comment
    if (line[0] == '#') {
      continue;
    }
    stringstream ss(line);
    while (getline(ss, line, '\t')) {
      if ((isdigit(line[0])) && (line.find("udp") != string::npos || line.find("tcp") != string::npos)) {
        service.insert(stoi(line));
        break;
      }
    }
  }

}

bool IsService(int port) {
  if (service.find(port) != service.end())
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

/*
 * Utility function to write multiple messages from a single stream
 */
bool writeDelimitedTo(
    const google::protobuf::MessageLite &message,
    google::protobuf::io::ZeroCopyOutputStream *rawOutput) {
  google::protobuf::io::CodedOutputStream output(rawOutput);

  // Write the size.
  const int size = message.ByteSize();
  output.WriteVarint32(size);

  uint8_t *buffer = output.GetDirectBufferForNBytesAndAdvance(size);
  if (buffer != NULL) {
    // Optimization:  The message fits in one buffer, so use the faster
    // direct-to-array serialization path.
    message.SerializeWithCachedSizesToArray(buffer);
  } else {
    // Slightly-slower path when the message is multiple buffers.
    message.SerializeWithCachedSizes(&output);
    if (output.HadError()) return false;
  }

  return true;
}

/*
 * Utility function to read multiple messages from a single stream
 */
bool readDelimitedFrom(
    google::protobuf::io::ZeroCopyInputStream *rawInput,
    google::protobuf::MessageLite *message) {
  google::protobuf::io::CodedInputStream input(rawInput);

  // Read the size.
  uint32_t size;
  if (!input.ReadVarint32(&size)) return false;

  // Tell the stream not to read beyond that size.
  auto limit = input.PushLimit(size);

  // Parse the message.
  if (!message->MergePartialFromCodedStream(&input)) return false;
  if (!input.ConsumedEntireMessage()) return false;

  // Release the limit.
  input.PopLimit(limit);

  return true;
}