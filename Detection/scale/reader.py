"""
Online Algorithm to detect services in NetFlow V5 records
"""
import argparse
import json
import sys
import flowtools

from bitarray import bitarray

import socket
import sys


nodes = 0
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
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 4242)
    try:
        sock.connect(server_address)
        print "Connected"
    finally:
        pass
    flows = flowtools.FlowSet(infile)
    laststat = 0
    dsts = dict()
    start = 0
    stop = 0
    avg = 0

    for flow in flows:
        flip = 0
        if (laststat == 0):
            laststat = flow.last
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
        time1 = flow.first
        time2 = flow.last
        if flow.tcp_flags > 63:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags & 63))
        else:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags))
        sc = 0
        uc = 0
        if (flow.prot == 6):
            fc = 1
            if (flags & SYN_ACK_PSH == SYN_ACK_PSH):
                sc = 1
            else:
                uc = 1
        elif (flow.prot == 17):
            fc = flow.dPkts
            if (flip == 1):
                sc = 1
            else:
                uc = 1
        else:
            continue
        dst = str(dst) + ":" + str(dport)
        src = str(src) + ":" + str(sport)
        # print src, dst, flow.first, flow.last
        # continue
        char = " -> "
        if (flip):
            char = " <- "
        # 1453395538.07 1453395578.14 164.76.136.0:51601 <- 54.230.88.0:80 5 260 0
        if (start == 0):
            start = time1
            stop = time1

            avg = time1
            dsts[int(start)] = dict()
        elif (time1 - stop > 1):
            avg = 0.9 * avg + 0.1 * time1
            if (avg - stop > 1):
                stop = avg
            #stash this
            continue
        elif (time1 - start > 1):  #reporting interval, currently 1 sec
            mes = json.dumps(dsts)
            mes = mes + "\n"
            try:
                sock.sendall(mes)
            finally:
                pass
            sock.recv(1024) # blocking call
            for d in dsts[int(start)]:
                print str(time1) + " " + str(d) + " " + str(dsts[int(start)][d])
            exit(0)
            start = time1
            dsts = dict()
            dsts[int(start)] = dict()
        stop = time1
        if dst not in dsts[int(start)]:
            dsts[int(start)][dst] = 0
        if (sc):
            dsts[int(start)][dst] = dsts[int(start)][dst] - fc
        else:
            dsts[int(start)][dst] = dsts[int(start)][dst] + fc
            #print str(time1) + " " + str(time2) + " " + str(src) + char + str(dst) + " " + str(flow.dPkts)+ " " + str(flow.dOctets) + " " + str(sc)


def main():
    nodes = 0
    parser = argparse.ArgumentParser(description="Detect heavy hitters from traces")

    parser.add_argument('-f', '--format', dest='file_format', nargs=1, default='None', choices=['nfdump', 'flow-tools'],
                        required=True, help='Trace format i.e. flow-tools or nfdump')
    parser.add_argument('infile', nargs='?', default=sys.stdin,
                        help='File path to read from. If no path is specified then defaults to stdin')
    args = parser.parse_args()
    trie = dict()
    """t.StringTrie(separator='.')
    """
    if (args.file_format[0] == "flow-tools"):
        getFlows(args.infile)


if __name__ == "__main__":
    main()
