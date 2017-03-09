import argparse
import flowtools
import pickle

__author__ = 'ameya'


def sort_flows(infile):
    flows = flowtools.FlowSet(infile)
    sorted_flows = []
    for f in flows:
        flow_dict = {
            "srcaddr": f.srcaddr,
            "dstaddr": f.dstaddr,
            "srcport": f.srcport,
            "dstport": f.dstport,
            "last": f.last,
            "tcp_flags": f.tcp_flags,
            "prot": f.prot,
            "dPkts": f.dPkts
        }
        sorted_flows.append(flow_dict)
    sorted_flows = sorted(sorted_flows, key=lambda x: x['last'])
    with open("test.pickle", "wb") as file_handler:
        pickle.dump(sorted_flows, file_handler)


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