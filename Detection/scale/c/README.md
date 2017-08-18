# Distributed Stream Processor

This section contains the code to read flow records exported in ASCII format using flow-export, aggregate them and send to the collector server. Google's protobuf is used for marshalling aggregated data and it needs to be installed to run the code. It is currently installed on the SENSS server but it can be easily installed on other machines using the instructions [here](https://github.com/google/protobuf/blob/master/src/README.md). 

### How to run?

First start the collector process with `./collector`

Next run reader(s).
This is the way to run the code for a single reader process:

```
flow-export -f2 -mDPKTS,DOCTETS,FIRST,LAST,SRCADDR,DSTADDR,SRCPORT,DSTPORT,PROT,TCP_FLAGS < /nfs_ds/users/mirkovic/nfs_ds/radb_ddos/WSUe/2016/2016-01/2016-01-22/ft-v05.2016-01-22.130020-0500 |  ./reader
```

The `f2` flag is used for the ASCII output format, `m` flag masks the binary data for only the specified fields (this greatly increases the speed of execution).

The code can be stopped using `ctrl/cmd + z` and there won't be any zombie processes.

### Code Style

We follow Google's C++ style standards as much as possible. Please refer [here](https://google.github.io/styleguide/cppguide.html) for reference.
