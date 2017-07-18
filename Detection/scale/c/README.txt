This is the way to run the code. 

flow-export -f2 -mDPKTS,DOCTETS,FIRST,LAST,SRCADDR,DSTADDR,SRCPORT,DSTPORT,PROT,TCP_FLAGS < /nfs_ds/users/mirkovic/nfs_ds/radb_ddos/WSUe/2016/2016-01/2016-01-22/ft-v05.2016-01-22.130020-0500 |  ./reader

Right now it will print stats for one specific subnet but in general it should get all the stats and send to collector. Collector should store stats per home and foreign and per timestamp. So pretty much I would make its storage very similar to "records.cc" but instead of map of iprange,cell I would use map of iprange,timedcell where timedcell is vector or map of cells, one for each timestamp. You will also need to know for each time if you got all the reports from readers, e.g., there are 29 readers in radb so you expect to hear from all of them. Once you hear from them all you can process cells up to that time. 
