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
from heapq import heappush, heappop
from time import sleep

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
HEAP_SIZE = 10000


class Client(asyncore.dispatcher):
    def __init__(self, host_address, name, flows):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.connect(host_address)
        self.outbox = deque()
        self.flows = flows
        self.start = 0
        self.stop = 0
        self.end_flag = False
        self.destinations = {}
        self.flow_heap = []
        self.reqs1 = 0
        self.reps1 = 0
        self.reqs2 = 0
        self.reps2 = 0
        self.total_reqs = 0
        self.fh = open("reader_print.txt", "a")
        self.fh_flow = open("flow_check/" + self.name, "a")
        self.send_single_flow(size=1000)

    def say(self, message):
        self.outbox.append(message)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        while message != "":
            sent_bytes = self.send(message)
            message = message[sent_bytes:]

    def handle_read(self):
        message = self.recv(1000)
        message_list = message.split("\t")
        self.fh_flow.write(str(message_list) + "\n")
        for message in message_list:
            if message == self.name:
                result = self.send_single_flow()
                if result == False:
                    # self.fh.write(self.name + " " + str(self.reqs1) + " " + str(self.reps1) + "\n")
                    self.fh.write(self.name + " " + str(self.reqs2) + " " + str(self.reps2) + "\n")
                    self.fh.write(self.name + " " + str(self.total_reqs) + "\n")
                    self.say("close")
                    sleep(2)
                    self.close()
                    raise asyncore.ExitNow()

    def send_single_flow(self, size=100):
        global HEAP_SIZE

        def get_next_flow(current_last=None):
            try:
                flow = self.flows.next()
                self.total_reqs += 1
                if current_last:
                    if int(flow.last) < current_last:
                        self.fh_flow.write("exceed\n")
                        get_next_flow(current_last=current_last)
                        return
                flow_tuple = (
                    int(flow.last),
                    flow.srcaddr,
                    flow.dstaddr,
                    flow.srcport,
                    flow.dstport,
                    flow.tcp_flags,
                    flow.prot,
                    flow.dPkts
                )
                heappush(self.flow_heap, flow_tuple)
            except:
                self.end_flag = True

        start = 0
        aggregated_dsts = []
        while True:
            while len(self.flow_heap) < HEAP_SIZE:
                if not self.end_flag:
                    get_next_flow()
                else:
                    break
            try:
                current_flow = heappop(self.flow_heap)
            except IndexError as e:
                if len(aggregated_dsts) > 0:
                    mes = json.dumps(aggregated_dsts)
                    mes += "\n"
                    self.say(mes)
                    break
                else:
                    return False
            get_next_flow(current_last=current_flow[0])
            flow_last = current_flow[0]
            flow_srcaddr = current_flow[1]
            flow_dstaddr = current_flow[2]
            flow_srcport = current_flow[3]
            flow_dstport = current_flow[4]
            flow_tcp_flags = current_flow[5]
            flow_prot = current_flow[6]
            flow_dPkts = current_flow[7]

            flip = False
            if flow_dstport in WELL_KNOWN_PORTS and flow_srcport not in WELL_KNOWN_PORTS:
                src = flow_srcaddr
                dst = flow_dstaddr
                sport = flow_srcport
                dport = flow_dstport
            elif flow_dstport not in WELL_KNOWN_PORTS and flow_srcport in WELL_KNOWN_PORTS:
                src = flow_dstaddr
                dst = flow_srcaddr
                sport = flow_dstport
                dport = flow_srcport
                flip = True
            else:
                continue

            if flow_tcp_flags > 63:
                flags = bitarray('{0:06b}'.format(flow_tcp_flags & 63))
            else:
                flags = bitarray('{0:06b}'.format(flow_tcp_flags))
            success_count = 0
            unsuccessful_count = 0
            if flow_prot == 6:
                flow_count = 1
                if flags & SYN_ACK_PSH == SYN_ACK_PSH:
                    success_count = 1
                else:
                    unsuccessful_count = 1
            elif flow_prot == 17:
                flow_count = flow_dPkts
                if flip:
                    success_count = 1
                else:
                    unsuccessful_count = 1
            else:
                continue
            src = str(src) + ":" + str(sport)
            dst = str(dst) + ":" + str(dport)

            # if dst == "207.75.112.0:53":
            #self.fh_flow.write(str(flow_last) + "\t" + src + "\t" + dst + "\t" + str(flow_dPkts) + "\n")

            if start == 0:
                start = flow_last
                # stop = time1
                # avg = time1
                dsts = dict()
            elif flow_last - start >= 1:  # reporting interval, currently 1 sec
                # push the current flow back to heap
                heappush(self.flow_heap, current_flow)
                """
                if "198.108.0.0:53" in dsts:
                    self.reqs1 += dsts['198.108.0.0:53']['q']
                    self.reps1 += dsts['198.108.0.0:53']['p']
                """
                if "207.75.112.0:53" in dsts:
                    self.reqs2 += dsts['207.75.112.0:53']['q']
                    self.reps2 += dsts['207.75.112.0:53']['p']

                aggregated_dsts.append({'reader': self.name, 'time': start, 'destinations': dsts})
                if len(aggregated_dsts) >= 100:
                    mes = json.dumps(aggregated_dsts)
                    mes += "\n"
                    self.say(mes)
                    aggregated_dsts = []
                    break
                # start = time2
                dsts = dict()
            # stop = time1

            """
            elif (time1 - stop > 1):
                avg = 0.9 * avg + 0.1 * time1
                if (avg - stop > 1):
                    stop = avg
                # stash this
                continue
            """

            #if dst == "207.75.112.0:53":
            #self.total_reqs += 1

            if dst not in dsts:
                dsts[dst] = {"q": 0, "p": 0}
            if success_count:
                dsts[dst]['p'] = dsts[dst]['p'] + flow_count
            else:
                dsts[dst]['q'] = dsts[dst]['q'] + flow_count
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
        # getFlows(args.infile)
        flow_dir = args.infile.split("/")[6]
        # Create a TCP/IP socket
        server_address = ('localhost', 4242)
        flows = flowtools.FlowSet(args.infile)
        client_socket = Client(server_address, flow_dir, flows)
        try:
            asyncore.loop(timeout=1)
        except asyncore.ExitNow, e:
            pass
        print "close"


if __name__ == "__main__":
    main()
    # main_reader()
