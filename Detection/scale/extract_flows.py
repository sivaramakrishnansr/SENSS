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
        
def getFlows(infile):
    flows = flowtools.FlowSet(infile)
    laststat = 0
    
    for flow in flows:
        flip=0
        time1 = flow.first
        time2 = flow.last
        if (laststat == 0):
            laststat = flow.last;
        #if flow.dstport in WELL_KNOWN_PORTS and flow.srcport not in WELL_KNOWN_PORTS:
        src = flow.srcaddr
        dst = flow.dstaddr
        sport = flow.srcport
        dport = flow.dstport
        if flow.dstport not in WELL_KNOWN_PORTS and flow.srcport in WELL_KNOWN_PORTS:
        #    src = flow.dstaddr
        #    dst = flow.srcaddr
        #    sport = flow.dstport
        #    dport = flow.srcport
            flip = 1
        #else:
        #    continue
        if flow.tcp_flags > 63:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags & 63))
        else:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags))
        sc = 0
        uc = 0
        if (flow.prot == 6):
            if (flags & SYN_ACK_PSH == SYN_ACK_PSH):
                sc = 1
            else:
                uc = 1
        elif(flow.prot == 17):
            if (flip == 1):
                sc = 1
            else:
                uc = 1
        else:
            continue
        #dst = str(dst) + ":" + str(dport)
        #src = str(src) + ":" + str(sport)
        char = " -> "
        if (flip):
            char = " <- "
        if (dst == "207.75.112.0" or src == "207.75.112.0"):
            print str(time1) + " " + str(time2) + " " + str(src) + ":" + str(sport) + char + str(dst) + ":" + str(dport) + " " + str(flow.dPkts)+ " " + str(flow.dOctets) + " " + str(sc);

            

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
        getFlows(args.infile)
    else:
        pass


if __name__ == "__main__":
    main()
