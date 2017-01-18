"""
Online Algorithm to detect services in NetFlow V5 records
"""
import argparse
import json
import sys
import pprint

def main():
    fp=open('data.json', 'r')
    data=json.load(fp)
    for d in data:
        print d
        for dst in data[d]:
            print str(dst) + " " + str(data[d][dst])

if __name__ == "__main__":
    main()
