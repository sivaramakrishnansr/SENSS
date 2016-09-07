"""
Online Algorithm to detect heavy hitters in NetFlow V5 records. Incomplete
"""
import argparse
import sys
import flowtools
import pygtrie as t
from bitarray import bitarray

WELL_KNOWN_PORTS = [19, 22, 23, 25, 80, 443]
SYN_ACK_PSH = bitarray('011010')
SYN_ACK_PSH_FIN = bitarray('000010')
SYN_ACK_FIN = bitarray('010011')
SYN_ACK_URG = bitarray('110010')
SYN_ACK_URG_FIN = bitarray('110011')
ACK_PSH = bitarray('011000')
ACK_FIN = bitarray('010001')

class DestInfo():
    def __init__(self, ls, sc, uc, mb, dur):
        self.last_seen = ls
        self.successful_cnxns = sc
        self.unsuccessful_cnxns = uc
        self.mega_bytes = mb
        self.duration = dur
        #self.state = st


def buildFlowToolsTrie(infile, trie):
    flows = flowtools.FlowSet(infile)

    for flow in flows:
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
            percent_uc = float(trie[dst].unsuccessful_cnxns)/float(trie[dst].unsuccessful_cnxns + trie[dst].successful_cnxns)
            if (trie[dst].unsuccessful_cnxns + trie[dst].successful_cnxns) > 100 and percent_uc > 0.1:
                print "Destination Address: " + dst + "\t Successful Connections " + str(trie[dst].successful_cnxns) \
                      + " Unsuccessful Connections: " + str(trie[dst].unsuccessful_cnxns) + "\t Percentage Unsuccessful "+str(percent_uc*100) + " %" #" \t Bytes per second: " + str(float(trie[dst].mega_bytes)/float(trie[dst].duration))

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
