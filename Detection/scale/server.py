#!/usr/bin/python
# A simple example of a threaded TCP server in Python.
#
# Copyright (c) 2012 Benoit Sigoure  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# - Neither the name of the StumbleUpon nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
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
import pickle
from threading import Thread, Timer
import time
from collections import defaultdict
import gc


curtime = 0
lasttime = 0
dict_dst_count = 0
file_count = 0
prev_dict_save = 0
client_arr = []
timestamp_queue = []
attacks = []
last_timestamp_recd = defaultdict(int)
timestamps = defaultdict(set)
min_timestamp = int(time.time())

DETINT = 100
reports_count = 29
new_start = False

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
            if stats[t]['destinations'][destination] > 20:
                print "attack on " + str(destination) + " at time " + str(t) + " count " + str(
                    stats[t]['destinations'][destination])
    stats = dict()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        global stats, curtime, lasttime, file_count, prev_dict_save, dict_dst_count, timestamp_queue, \
            last_timestamp_recd, timestamps, new_start, min_timestamp
        while True:
            # prev_dict_save = int(time.time())
            mes = self.rfile.readline()
            try:
                if new_start:
                    print "new"
                    new_start = False
            except:
                pass
            # new_start = False
            if not mes:  # EOF
                break
            try:
                data = json.loads(mes)
            except:
                print mes
                save_dict()
                # self.wfile.write("OK")
                print "done"
                new_start = True
                break
            """
            temp_count = 0
            if self.client_address[1] not in client_arr:
                client_arr.append(self.client_address[1])
            """
            prev_dict_save = int(time.time())
            t = int(data['time'])
            last_timestamp_recd[data['reader']] = max(last_timestamp_recd[data['reader']], t)
            min_timestamp_key = min(last_timestamp_recd, key=last_timestamp_recd.get)
            min_timestamp = last_timestamp_recd[min_timestamp_key]
            timestamp_flag = False
            # timestamps[t].add(self.client_address[1])
            if 'destinations' in stats[file_count][t]:
                # print "append"
                if self.client_address[1] not in stats[file_count][t]['clients']:
                    stats[file_count][t]['clients'].append(self.client_address[1])
                    if len(stats[file_count][t]['clients']) >= 29:
                        timestamp_flag = True
                        # stats[file_count][t]['reports'] += 1
            else:
                """
                        if dict_dst_count >= 5000000:
                            dict_dst_count = 0
                            file_count += 1
                            stats.append(defaultdict(dict))
                            # timestamps.append(defaultdict(dict))
                            file_name = "dump-" + str(file_count - 1) + ".pickle"
                            dump_dictionary(file_name, file_count - 1)
                            print "saved"
                """
                stats[file_count][t]['destinations'] = dict()
                stats[file_count][t]['clients'] = [self.client_address[1]]

            for dst in data['destinations']:
                if dst in stats[file_count][t]['destinations']:
                    # timestamps[file_count][t][dst][1] = time.time()
                    stats[file_count][t]['destinations'][dst] += data['destinations'][dst]
                else:
                    # current_time = time.time()
                    # timestamps[file_count][t][dst] = [current_time, current_time]
                    stats[file_count][t]['destinations'][dst] = data['destinations'][dst]
                    # dict_dst_count += 1
            if timestamp_flag:
                timestamp_queue.append(t)

            """
                if t > curtime:
                    stats[t] = dict()
                    stats[t]['destinations'] = dict()
                    stats[t]['rep   orts'] = 1
                    # if first time data received, set curtime and lasttime
                    if curtime == 0 and lasttime == 0:
                        curtime = t
                        lasttime = t
                    curtime = t
                else:
                    try:
                        stats[t]['reports'] += 1
                    except KeyError as e:
                        print "curtime: " + str(curtime) + " t: " + str(t)
                try:
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
                    # detect()
                except:
                    pass
            """
            # send OK to client
            # self.wfile.write("OK")


def dump_dictionary(file_name, index):
    global stats, timestamps, attacks
    # for t in stats[index]:
    # if 'clients' in stats[index][t]:
    # stats[index][t]['reports'] = len(stats[index][t]['clients'])
    # del stats[index][t]['clients']
    with open(file_name, 'wb') as handle:
        pickle.dump(attacks, handle)
        del attacks
        gc.collect()
        attacks = []
    """cd
    with open(file_name, 'wb') as handle:
        pickle.dump(stats[index], handle)
        stats[index].clear()
        print "gc = " + str(gc.collect())
    """
    # with open('t-' + file_name, 'wb') as handle:
    # pickle.dump(timestamps[index], handle)


def save_dict():
    global stats, prev_dict_save, file_count, client_arr, attacks, timestamps, min_timestamp, last_timestamp_recd
    # Timer(10.0, save_dict).start()
    print len(attacks)
    # print "arr: " + str(len(client_arr))
    if len(attacks) > 0:
        print "inside"
        prev_dict_save = int(time.time())
        file_name = "attack-dump-" + str(file_count) + ".pickle"
        dump_dictionary(file_name, None)
        # stats.append(defaultdict(dict))
        stats[file_count].clear()
        del stats
        gc.collect()
        stats = [defaultdict(dict)]
        min_timestamp = time.time()
        del last_timestamp_recd
        last_timestamp_recd = defaultdict(int)
        print "saved"
    """
    if len(stats[file_count]) > 0 and int(time.time()) - prev_dict_save > 10:
        prev_dict_save = int(time.time())
        file_name = "dump-" + str(file_count) + ".pickle"
        file_count += 1
        stats.append(defaultdict(dict))
        dump_dictionary(file_name, file_count)
        #stats.append(defaultdict(dict))
        print "saved"
    """


def consume_completed_timestamps():
    global stats, timestamp_queue, file_count, attacks, dict_dst_count
    Timer(5.0, consume_completed_timestamps).start()
    # print "Timestamp queue: " + str(len(timestamp_queue))
    len_t = len(timestamp_queue)
    for i in range(len_t):
        t = timestamp_queue[i]
        for dst in stats[file_count][t]['destinations']:
            if stats[file_count][t]['destinations'][dst] >= 10:
                attacks.append({"timestamp": t, "dst": dst})
        dict_dst_count -= len(stats[file_count][t]['destinations'])
        del stats[file_count][t]
    del timestamp_queue[0: len_t]


def consume_time_exceed_timestamps():
    global stats, last_timestamp_recd, file_count, attacks, DETINT, dict_dst_count
    Timer(10.0, consume_time_exceed_timestamps).start()
    stats_t = stats[file_count].iterkeys()
    stats_t = sorted(stats_t)
    for t in stats_t:
        if t % 50 == 0:
            print min_timestamp - t
        if min_timestamp - t >= DETINT:
            for dst in stats[file_count][t]['destinations']:
                if stats[file_count][t]['destinations'][dst] >= 10:
                    attacks.append({"timestamp": t, "dst": dst, "flow_count": stats[file_count][t]['destinations'][dst],
                                    "clients": len(stats[file_count][t]['clients'])})
            # dict_dst_count -= len(stats[file_count][t]['destinations'])
            del stats[file_count][t]
        else:
            break


stats = [defaultdict(dict)]


def main():
    # save_dict()
    consume_completed_timestamps()
    consume_time_exceed_timestamps()
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
