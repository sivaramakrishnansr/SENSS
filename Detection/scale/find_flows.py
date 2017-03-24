import argparse
import flowtools
import pickle
import sys
from bitarray import bitarray

__author__ = 'ameya'

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


def sort_flows(infile):
    flows = flowtools.FlowSet(infile)
    replies = 0
    requests = 0
    fh = open("chi-600e_check.txt", "a")
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

        dst = str(dst) + ":" + str(dport)
        if dst != "198.108.0.0:53":
            continue

        if flow.tcp_flags > 63:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags & 63))
        else:
            flags = bitarray('{0:06b}'.format(flow.tcp_flags))
        success_count = 0
        unsuccessful_count = 0
        if flow.prot == 6:
            flow_count = 1
            if flags & SYN_ACK_PSH == SYN_ACK_PSH:
                success_count = 1
            else:
                unsuccessful_count = 1
        elif flow.prot == 17:
            flow_count = flow.dPkts
            if flip:
                success_count = 1
            else:
                unsuccessful_count = 1
        else:
            continue

        fh.write(str(flow.srcaddr) + ":" + str(flow.srcport) + "\t" + str(flow.dstaddr) + ":" + str(
            flow.dstaddr) + "\t" + str(flow_count))

        if success_count:
            replies += flow_count
        else:
            requests += flow_count

    # fh = open("chi-600e_all_times", "a")
    # fh.write(infile.split('/')[10] + "\t" + str(requests) + "\t" + str(replies) + "\n")
    fh.close()


def main():
    parser = argparse.ArgumentParser(description="Detect heavy hitters from traces")

    parser.add_argument('-f', '--format', dest='file_format', nargs=1, default='None', choices=['nfdump', 'flow-tools'],
                        required=True, help='Trace format i.e. flow-tools or nfdump')
    parser.add_argument('infile', nargs='?', default=sys.stdin,
                        help='File path to read from. If no path is specified then defaults to stdin')
    args = parser.parse_args()
    sort_flows(args.infile)


if __name__ == "__main__":
    main()