#!/usr/bin/python
# A simple example of a threaded TCP server in Python.
#
# Copyright (c) 2012 Benoit Sigoure  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#   - Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   - Neither the name of the StumbleUpon nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import SocketServer
import json
from threading import Thread
from time import sleep

curtime = 0
lasttime = 0

DETINT = 10
reports_count = 29

'''
# Old Detection Module
def detect():
    global stats, curtime, lasttime

    while True:
        diff = curtime - lasttime
        print "curtime " + str(curtime) + " lasttime " + str(lasttime) + " diff" + str(diff)
        if (int(curtime - lasttime) > DETINT):
            print "Will detect "
            ot = curtime
            newstats = dict(stats)
            for t in newstats:
                if t > lasttime + DETINT and lasttime > 0:
                    continue
                for dst in stats[t]:
                    if (stats[t][dst] > 0):
                        print "attack on " + str(dst) + " at time " + str(t) + " stats " + str(stats[t][dst])
                del stats[t]
                lasttime = ot
        sleep(1)

'''


def detect():
    global stats, curtime, lasttime
    for t in stats:
        for destination in stats[t]['destinations']:
            if stats[t]['destinations'][destination] > 0:
                print "attack on " + str(destination) + " at time " + str(t) + " count " + str(
                    stats[t]['destinations'][destination])
    stats = dict()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        global stats, curtime, lasttime
        while True:
            mes = self.rfile.readline()
            if not mes:  # EOF
                break
            data = json.loads(mes)
            for d in data:
                t = int(d)
                if t > curtime:
                    stats[t] = dict()
                    stats[t]['destinations'] = dict()
                    stats[t]['reports'] = 1
                    # if first time data received, set curtime and lasttime
                    if curtime == 0 and lasttime == 0:
                        curtime = t
                        lasttime = t
                    curtime = t
                else:
                    stats[t]['reports'] += 1
                for dst in data[d]:
                    if dst not in stats[t]['destinations']:
                        stats[t]['destinations'][dst] = 0
                    stats[t]['destinations'][dst] += data[d][dst]
                # check if all reports obtained
                if stats[t]['reports'] == reports_count:
                    lasttime = t
                    # all reports obtained. Run the detection module
                    detect()
                elif t - lasttime >= DETINT:
                    lasttime = t
                    # limit exceeded. Run the detection module
                    detect()


stats = dict()


def main():
    server = ThreadedTCPServer(("0.0.0.0", 4242), Handler)
    try:
        thread = Thread()
        thread.start()
        server.serve_forever()
        thread.join()


    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
