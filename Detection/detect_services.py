"""
Online Algorithm to detect services in NetFlow V5 records
"""
import argparse
import sys
import flowtools
import pygtrie as t
from bitarray import bitarray

nodes=0
WELL_KNOWN_PORTS = [19, 22, 23, 25, 53, 80, 443]
SYN_ACK_PSH = bitarray('011010')
SYN_ACK_PSH_FIN = bitarray('000010')
SYN_ACK_FIN = bitarray('010011')
SYN_ACK_URG = bitarray('110010')
SYN_ACK_URG_FIN = bitarray('110011')
ACK_PSH = bitarray('011000')
ACK_FIN = bitarray('010001')
PERIOD = 60
DELPERIOD = 600

class DestInfo():
    def __init__(self, ls, sc, uc, mb, dur):
        self.last_seen = ls
        self.successful_cnxns = sc
        self.unsuccessful_cnxns = uc
        self.duration = dur
        
def printFlows(trie, timenow):
    global nodes
    print "Nodes " + str(nodes)
    for dst in trie.keys():
        if (timenow - trie[dst].last_seen > DELPERIOD):
            del trie[dst]
            nodes -= 1
            continue
        if (trie[dst].successful_cnxns == 0):
            continue
        dur = trie[dst].duration/trie[dst].successful_cnxns;
        print "Destination: " + dst + "\t Successful: " + str(trie[dst].successful_cnxns) \
                + " Unsuccessful: " + str(trie[dst].unsuccessful_cnxns) + "Avg dur: " + str(dur)
        trie[dst].successful_cnxns = 0;
        trie[dst].unsuccessful_cnxns = 0;
        trie[dst].duration = 0

def buildFlowToolsTrie(infile, trie):
    global nodes
    flows = flowtools.FlowSet(infile)
    laststat = 0;
    
    for flow in flows:
        if (laststat == 0):
            laststat = flow.last;
        if (flow.first - laststat > PERIOD):
            printFlows(trie, flow.last);
            laststat = flow.last;
        if flow.dstport not in WELL_KNOWN_PORTS:
            continue
        if flow.tcp_flags > 63:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags & 63))
        else:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags))

        sc=0
        uc=0
        if (flow.prot == 6):
            if (flags & SYN_ACK_PSH == SYN_ACK_PSH):
                sc=1
            else:
                uc=1
        elif(flow.prot == 17):
            if (
        dst = str(flow.dstaddr) + ":" + str(flow.dstport)
        if(dst not in trie):
            trie[dst] = DestInfo(ls=flow.last, sc=sc,uc=uc,mb=float(flow.dOctets)/1000000,dur=float(flow.last-flow.first))
            nodes += 1
        else:
            trie[dst].last_seen = flow.last
            trie[dst].successful_cnxns += sc
            trie[dst].unsuccessful_cnxns += uc
            if sc:
                trie[dst].duration +=float(flow.last-flow.first)

            

def main():

    nodes = 0
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
