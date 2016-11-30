"""
Online Algorithm to detect heavy hitters in NetFlow V5 records. Incomplete
"""
import argparse
import sys
import flowtools
import pygtrie as t
from bitarray import bitarray

WELL_KNOWN_PORTS = [19, 22, 23, 25, 53, 80, 443]
SYN_ACK_PSH = bitarray('011010')
SYN_ACK_PSH_FIN = bitarray('000010')
SYN_ACK_FIN = bitarray('010011')
SYN_ACK_URG = bitarray('110010')
SYN_ACK_URG_FIN = bitarray('110011')
ACK_PSH = bitarray('011000')
ACK_FIN = bitarray('010001')
PERIOD = 60
alpha = 0.8

class DestInfo():
    def __init__(self, ls, sc, uc, mb, dur):
        self.last_seen = ls
        self.successful_cnxns = sc
        self.unsuccessful_cnxns = uc
        self.successful_lvl = 0
        self.unsuccessful_lvl = 0
        self.mega_bytes = mb    
        self.duration = dur
        self.rate = 0
        self.rate_lvl = 0
        #self.state = st

def printFlows(trie):        
    for dst in trie:
        if (trie[dst].unsuccessful_cnxns + trie[dst].successful_cnxns == 0):
            continue;
        percent_uc = float(trie[dst].unsuccessful_cnxns)/float(trie[dst].unsuccessful_cnxns + trie[dst].successful_cnxns)
        rate = 100*float(trie[dst].mega_bytes)/float(trie[dst].duration);
        conns = trie[dst].successful_cnxns + trie[dst].unsuccessful_cnxns
        if (percent_uc > trie[dst].unsuccessful_lvl*1.5 and trie[dst].successful_lvl > trie[dst].successful_cnxns*2 and trie[dst].rate_lvl*2 < rate and conns > 100):
            print "Destination Address: " + dst + "\t Successful Connections " + str(trie[dst].successful_cnxns) \
                + " historically " + str(trie[dst].successful_lvl) + " Unsuccessful Connections: " + str(trie[dst].unsuccessful_cnxns) + "\t Percentage Unsuccessful "+str(percent_uc*100) + " historically " + str(trie[dst].unsuccessful_lvl) + " %\t Bytes per second: " + str(100*float(trie[dst].mega_bytes)/float(trie[dst].duration)) + " historically " +  str(trie[dst].rate_lvl) 
        trie[dst].successful_lvl =  trie[dst].successful_lvl*alpha + trie[dst].successful_cnxns*(1-alpha)
        trie[dst].unsuccessful_lvl =  trie[dst].unsuccessful_lvl*alpha + percent_uc*100*(1-alpha)
        trie[dst].rate_lvl =  trie[dst].rate_lvl*alpha + 100*float(trie[dst].mega_bytes)/float(trie[dst].duration)*(1-alpha)
        trie[dst].successful_cnxns = 0;
        trie[dst].unsuccessful_cnxns = 0;
        trie[dst].mega_bytes = 0
        trie[dst].duration = 0

def buildFlowToolsTrie(infile, trie):
    flows = flowtools.FlowSet(infile)
    laststat = 0;
    
    for flow in flows:
        if (laststat == 0):
            laststat = flow.first;
        if (flow.first - laststat > PERIOD):
            printFlows(trie);
            laststat = flow.first;
        if flow.prot!=6 or flow.dstport not in WELL_KNOWN_PORTS:
            continue
        if flow.last - flow.first < 15:
            continue
        if flow.tcp_flags > 63:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags & 63))
        else:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags))

        sc=0
        uc=0
        if (flags & SYN_ACK_PSH == SYN_ACK_PSH) or (flags & SYN_ACK_PSH_FIN == SYN_ACK_PSH_FIN)\
                or (flags & SYN_ACK_FIN == SYN_ACK_FIN) or (flags & SYN_ACK_URG == SYN_ACK_URG)\
                or (flags & SYN_ACK_URG_FIN == SYN_ACK_URG_FIN):
            sc=1
        else:
            uc=1
            time = float(flow.last - flow.first)
        dst = str(flow.dstaddr)
        src = str(flow.srcaddr)
        if(dst not in trie and src not in trie):
            trie[dst] = DestInfo(ls=flow.last, sc=sc,uc=uc,mb=float(flow.dOctets)/1000000,dur=float(flow.last-flow.first))
        else:
            if(src in trie):
                dst = src
            trie[dst].last_seen = flow.last
            trie[dst].successful_cnxns += sc
            trie[dst].unsuccessful_cnxns += uc
            trie[dst].mega_bytes += float(flow.dOctets)/1000000
            trie[dst].duration +=float(flow.last-flow.first)

            

def main():

    parser = argparse.ArgumentParser(description="Detect heavy hitters from traces")

    parser.add_argument('-f','--format',dest='file_format',nargs=1,default='None',choices=['nfdump','flow-tools'],required=True,help='Trace format i.e. flow-tools or nfdump')
    parser.add_argument('infile',nargs='?',default=sys.stdin,help='File path to read from. If no path is specified then defaults to stdin')
    args = parser.parse_args()
    trie = t.StringTrie(separator='.')
    if(args.file_format[0] == "flow-tools"):
        buildFlowToolsTrie(args.infile, trie)
    else:
        pass


if __name__ == "__main__":
    main()
