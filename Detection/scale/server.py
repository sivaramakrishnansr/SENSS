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

import asyncore
import socket
import json
import pickle
from threading import Thread, Timer
import time
from collections import defaultdict
import gc


curtime = 0
lasttime = 0
dict_dst_count = 0
# file_count = 0
prev_dict_save = 0
client_arr = []
timestamp_queue = []
attacks = []
last_timestamp_recd = defaultdict(int)
timestamps = defaultdict(set)
min_timestamp = 0
save_lock = False
file_count1 = 0

DETINT = 5
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


def store_attacks():
    save_dict()
    # time.sleep(5)
    return True


class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        global stats, curtime, lasttime, prev_dict_save, dict_dst_count, timestamp_queue, \
            last_timestamp_recd, timestamps, new_start, min_timestamp
        while True:
            # prev_dict_save = int(time.time())
            mes = self.recv(1000000)
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
                if mes == "Done":
                    print "all done"
                    min_timestamp = int(time.time())
                    consume_time_exceed_timestamps()
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
            # print len(last_timestamp_recd)
            if len(last_timestamp_recd) >= 29:
                # print "update min_timestamp"
                min_timestamp_key = min(last_timestamp_recd, key=last_timestamp_recd.get)
                min_timestamp = last_timestamp_recd[min_timestamp_key]
            timestamp_flag = False
            # timestamps[t].add(self.client_address[1])
            if 'destinations' in stats[t]:
                # print "append"
                if self.addr not in stats[t]['clients']:
                    stats[t]['clients'].append(self.addr)
                    if len(stats[t]['clients']) >= 29:
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
                stats[t]['destinations'] = dict()
                stats[t]['clients'] = [self.addr]

            for dst in data['destinations']:
                if dst in stats[t]['destinations']:
                    # timestamps[file_count][t][dst][1] = time.time()
                    stats[t]['destinations'][dst] += data['destinations'][dst]
                else:
                    # current_time = time.time()
                    # timestamps[file_count][t][dst] = [current_time, current_time]
                    stats[t]['destinations'][dst] = data['destinations'][dst]
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
    # with open("stats_dump.pickle", "wb") as handle:
    #     pickle.dump(stats[file_count], handle)

    """cd
    with open(file_name, 'wb') as handle:
        pickle.dump(stats[index], handle)
        stats[index].clear()
        print "gc = " + str(gc.collect())
    """
    # with open('t-' + file_name, 'wb') as handle:
    # pickle.dump(timestamps[index], handle)


def save_dict(erase=True):
    global stats, prev_dict_save, client_arr, attacks, timestamps, min_timestamp, last_timestamp_recd, save_lock, file_count1
    # Timer(10.0, save_dict).start()
    save_lock = True
    print len(attacks)
    # print "arr: " + str(len(client_arr))
    if len(attacks) > 0:
        print "inside"
        prev_dict_save = int(time.time())
        file_name = "attack-dump-" + str(file_count1) + ".pickle"
        dump_dictionary(file_name, None)
        file_count1 += 1
        # stats.append(defaultdict(dict))
        # stats[file_count].clear()
        # del stats
        #gc.collect()
        #stats = [defaultdict(dict)]
        if erase:
            min_timestamp = 0
            del last_timestamp_recd
            last_timestamp_recd = defaultdict(int)
        print "saved"
    save_lock = False
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
    global stats, timestamp_queue, attacks, dict_dst_count, save_lock
    Timer(5.0, consume_completed_timestamps).start()
    if save_lock:
        return True
    # print "Timestamp queue: " + str(len(timestamp_queue))
    len_t = len(timestamp_queue)
    for i in range(len_t):
        t = timestamp_queue[i]
        for dst in stats[t]['destinations']:
            if stats[t]['destinations'][dst] >= 10:
                attacks.append({"timestamp": t, "dst": dst})
        dict_dst_count -= len(stats[t]['destinations'])
        del stats[t]
    del timestamp_queue[0: len_t]


def consume_time_exceed_timestamps():
    global stats, last_timestamp_recd, attacks, DETINT, dict_dst_count, save_lock
    Timer(10.0, consume_time_exceed_timestamps).start()
    if save_lock:
        return True
    print "attacks: " + str(len(attacks))
    # if len(attacks) >= 1000000:
    #save_dict(erase=False)
    stats_t = stats.iterkeys()
    stats_t = sorted(stats_t)
    print len(stats)
    print min_timestamp
    for t in stats_t:
        if min_timestamp - t >= DETINT:
            if 'destinations' not in stats[t]:
                del stats[t]
                continue
            for dst in stats[t]['destinations']:
                if stats[t]['destinations'][dst] >= 10:
                    attacks.append({"timestamp": t, "dst": dst, "flow_count": stats[t]['destinations'][dst],
                                    "clients": len(stats[t]['clients'])})
            # dict_dst_count -= len(stats[file_count][t]['destinations'])
            del stats[t]
        else:
            break
    print "remaining: " + str(len(stats))


stats = defaultdict(dict)


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(30)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)


def main():
    # save_dict()
    consume_completed_timestamps()
    consume_time_exceed_timestamps()
    server = EchoServer('localhost', 4242)
    asyncore.loop()


if __name__ == "__main__":
    main()
