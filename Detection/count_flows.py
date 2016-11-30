"""
Online Algorithm to detect services in NetFlow V5 records
"""
import argparse
import sys
import flowtools

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
    def __init__(self, ls):
        self.last_seen = ls
        self.uc_long = 0
        self.sc_long = 0
        self.uc = 0
        self.sc = 0
        self.periods = 0
        
def printFlows(trie, timenow):
    global nodes
    for dst in trie.keys():
        if timenow > 0:
            """print str(dst) + " flows " + str(trie[dst].flows)"""
            trie[dst].uc_long += trie[dst].uc
            trie[dst].sc_long += trie[dst].sc
            trie[dst].periods += 1
            trie[dst].uc = 0
            trie[dst].sc = 0
        elif (trie[dst].periods > 0):
            avgu = trie[dst].uc_long/trie[dst].periods
            avgs = trie[dst].sc_long/trie[dst].periods
            print str(dst) + " " + str(avgs) + " " + str(avgu)

def buildFlowToolsTrie(infile, trie):
    global nodes
    flows = flowtools.FlowSet(infile)
    laststat = 0
    
    for flow in flows:
        flip=0
        if (laststat == 0):
            laststat = flow.last;
        if (flow.first - laststat > PERIOD):
            printFlows(trie, flow.last);
            laststat = flow.last;
        if flow.dstport in WELL_KNOWN_PORTS and flow.srcport not in WELL_KNOWN_PORTS:
            src = flow.srcaddr
            dst = flow.dstaddr
            sport = flow.srcport
            dport = flow.dstport
        elif flow.dstport not in WELL_KNOWN_PORTS and flow.srcport in WELL_KNOWN_PORTS:
            src = flow.dstaddr
            dst = flow.srcaddr
            sport = flow.dstport
            dport = flow.srcport
            flip = 1
        else:
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
            if (flip == 1):
                sc=1
            else:
                uc=1
        else:
            continue
        dst = str(dst) + ":" + str(dport)

        if(dst not in trie):
            trie[dst] = DestInfo(ls=flow.last)
            nodes += 1
        trie[dst].sc += sc
        trie[dst].uc += uc
            

def main():

    nodes = 0
    parser = argparse.ArgumentParser(description="Detect heavy hitters from traces")

    parser.add_argument('-f','--format',dest='file_format',nargs=1,default='None',choices=['nfdump','flow-tools'],required=True,help='Trace format i.e. flow-tools or nfdump')
    parser.add_argument('infile',nargs='?',default=sys.stdin,help='File path to read from. If no path is specified then defaults to stdin')
    args = parser.parse_args()
    trie = dict()
    """t.StringTrie(separator='.')
    """
    if(args.file_format[0] == "flow-tools"):
        buildFlowToolsTrie(args.infile, trie)
    else:
        pass

    printFlows(trie, 0)

if __name__ == "__main__":
    main()
