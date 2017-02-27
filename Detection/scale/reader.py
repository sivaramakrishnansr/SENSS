"""
Online Algorithm to detect services in NetFlow V5 records
"""
import argparse
import json
import flowtools
from bitarray import bitarray
import socket
import sys
import asyncore
from collections import deque

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


class Client(asyncore.dispatcher):
    def __init__(self, host_address, name):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.connect(host_address)
        self.outbox = deque()

    def say(self, message):
        self.outbox.append(message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        self.send(message)

    def handle_read(self):
        message = self.recv(1000)
        return message


def getFlows(infile):
    flow_dir = infile.split("/")[6]
    # Create a TCP/IP socket
    server_address = ('localhost', 4242)
    client_socket = Client(server_address, flow_dir)
    flows = flowtools.FlowSet(infile)
    """
    for infile in infiles:
        flow_dir = infile.split("/")[6]
        flows.append((flow_dir, flowtools.FlowSet(infile)))
    """
    dsts = dict()
    start = 0
    stop = 0
    avg = 0

    for flow in flows:
        flip = False
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
            flip = True
        else:
            continue
        # time1 = flow.first
        time2 = flow.last
        if flow.tcp_flags > 63:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags & 63))
        else:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags))
        sc = 0
        uc = 0
        if flow.prot == 6:
            fc = 1
            if flags & SYN_ACK_PSH == SYN_ACK_PSH:
                sc = 1
            else:
                uc = 1
        elif flow.prot == 17:
            fc = flow.dPkts
            if flip:
                sc = 1
            else:
                uc = 1
        else:
            continue
        dst = str(dst) + ":" + str(dport)
        src = str(src) + ":" + str(sport)
        # print src, dst, flow.first, flow.last
        # continue

        # 1453395538.07 1453395578.14 164.76.136.0:51601 <- 54.230.88.0:80 5 260 0

        """
        elif (time1 - stop > 1):
            avg = 0.9 * avg + 0.1 * time1
            if (avg - stop > 1):
                stop = avg
            # stash this
            continue
        """
        if start == 0:
            start = time2
            # stop = time1

            # avg = time1
            dsts = dict()
        elif time2 - start > 1:  # reporting interval, currently 1 sec
            mes = json.dumps({'reader': infile.split('/')[6], 'time': start, 'destinations': dsts})
            mes += "\n"
            client_socket.say(mes)
            response = client_socket.handle_read()
            start = time2
            dsts = dict()
            # dsts[int(start)] = dict()
        # stop = time1
        if dst not in dsts:
            dsts[dst] = 0
        if (sc):
            dsts[dst] = dsts[dst] - fc
        else:
            dsts[dst] = dsts[dst] + fc
            # print str(time1) + " " + str(time2) + " " + str(src) + char + str(dst) + " " + str(flow.dPkts)+ " " + str(flow.dOctets) + " " + str(sc)
    """
    for t in sorted(dsts.iterkeys()):
        mes = json.dumps({'reader': infile.split('/')[6], 'time': t, 'destinations': dsts[t]})
        mes = mes + "\n"
        try:
            print "send " + str(infile.split("/")[6])
            sock.sendall(mes)
        finally:
            pass
    """


"""
def main_reader():
    getFlows(sys.argv[1:])
"""


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
    # main_reader()
