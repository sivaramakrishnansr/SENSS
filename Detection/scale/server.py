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
import asyncore
import socket
import json
import pickle
from threading import Thread, Timer
import time
from collections import defaultdict, deque
import gc
from heapq import heappush, heappop
from copy import deepcopy


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
min_timestamp = 0
save_lock = False
file_count1 = 0
heap = []
current_data = {}
current_timestamp = 0
backlog_consume = []
receive_buffer = ""
all_data = {}
fh1 = open("test_json.txt", "a")
closed_clients = []

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


class RemoteClient(asyncore.dispatcher):
    def __init__(self, host, client_socket, address):
        asyncore.dispatcher.__init__(self, client_socket)
        self.host = host
        self.outbox = deque()
        self.name = None
        self.rb = ""

    def writable(self):
        ''' It has point to call handle_write only when there's something in outbox
            Having this method always returning true will cause 100% CPU usage
        '''
        return bool(self.outbox)

    def say(self, message):
        self.outbox.append(message)

    def handle_read(self):
        global reports_count, receive_buffer, all_data, fh1, closed_clients, current_timestamp
        result = ""
        client_message = self.recv(999999999)
        # print "response"
        try:
            if self.rb != "":
                client_message = self.rb + client_message
                self.rb = client_message
            data = json.loads(client_message)
            # print "loaded"
            if self.name is None:
                self.name = data[0]['reader']
            if self.name not in all_data:
                all_data[self.name] = []
            # print len(data)
            for single_data in data:
                all_data[self.name].append((single_data['time'], single_data['destinations']))
            result = self.client_message_handle(data, reader_name=self.name, load_json=True)
            self.rb = ""
        except ValueError as e:
            # print e
            client_message = client_message.strip()
            if client_message == "close" or client_message == "":
                closed_clients.append(self.name)
                print "close"
                # reports_count -= 1
                result = self.client_message_handle("close", force_get_next=True)
            elif len(client_message) >= 20:
                if self.rb == "":
                    self.rb += client_message
            """
            else:
                self.host.all_close()
                result = self.client_message_handle(client_message)
            """
        if result == "all_close":
            self.host.all_close()
            consume_time_exceed_timestamps(current_timestamp)
            save_dict(force=True)
            print result
            return
        # print result
        self.host.broadcast(result)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        message += "\t"
        self.send(message)

    @staticmethod
    def client_message_handle(data, reader_name=None, load_json=False, force_get_next=False):
        global stats, curtime, lasttime, prev_dict_save, dict_dst_count, timestamp_queue, last_timestamp_recd, \
            timestamps, new_start, min_timestamp, heap, reports_count, current_data, current_timestamp, all_data, closed_clients
        # prev_dict_save = int(time.time())
        try:
            if new_start:
                print "new"
                new_start = False
        except:
            pass
        # new_start = False
        if not data:
            return ""
        if not load_json and not force_get_next:
            # TODO: There might be some timestamps in previous and next log file iterations
            print data
            print "not load json"
            consume_time_exceed_timestamps(current_timestamp)
            if data == "Done":
                print "all done"
            save_dict(force=True)
            print "done"
            new_start = True
            return ""
        if not force_get_next:
            # prev_dict_save = int(time.time())
            t = int(all_data[reader_name][0][0])
            heappush(heap, (t, reader_name))
            current_data[reader_name] = all_data[reader_name][0][1]
            del all_data[reader_name][0]
        if len(heap) < reports_count and data != "close":
            print "reader: " + str(reader_name)
            print len(all_data[reader_name])
            return ""
            # for reader in all_data:
            # print reader + " : " + str(len(all_data[reader]))
        j = 0
        while True:
            # print j
            # j += 1
            heap_element = heappop(heap)
            if current_timestamp == 0:
                current_timestamp = heap_element[0]
            elif heap_element[0] > current_timestamp:
                # detect attacks
                consume_time_exceed_timestamps(current_timestamp)
                current_timestamp = heap_element[0]
            data = current_data[heap_element[1]]
            if current_timestamp not in stats:
                stats[current_timestamp] = dict()

                # if len(data) > 100:
                #print len(data)

            for dst in data:
                if dst in stats[current_timestamp]:
                    stats[current_timestamp][dst][0] += data[dst]['q']
                    stats[current_timestamp][dst][1] += data[dst]['p']
                else:
                    stats[current_timestamp][dst] = [data[dst]['q'], data[dst]['p']]

            try:
                t = int(all_data[heap_element[1]][0][0])
                heappush(heap, (t, heap_element[1]))
                current_data[heap_element[1]] = all_data[heap_element[1]][0][1]
                del all_data[heap_element[1]][0]
            except IndexError as e:
                continue

            if len(all_data[heap_element[1]]) <= 90:
                if heap_element[1] not in closed_clients:
                    return heap_element[1]
                else:
                    if len(all_data[heap_element[1]]) > 0:
                        t = int(all_data[heap_element[1]][0][0])
                        heappush(heap, (t, heap_element[1]))
                        current_data[heap_element[1]] = all_data[heap_element[1]][0][1]
                        del all_data[heap_element[1]][0]
                    else:
                        reports_count -= 1
                        if reports_count == 0:
                            return "all_close"

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
        # return data['reader']


class Host(asyncore.dispatcher):
    def __init__(self, address=('localhost', 4242)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(29)
        self.remote_clients = []

    def handle_accept(self):
        client_socket, addr = self.accept()  # For the remote client.
        self.remote_clients.append(RemoteClient(self, client_socket, addr))

    def handle_read(self):
        pass

    def handle_close(self):
        global reports_count
        print "closed"
        reports_count -= 1

    def broadcast(self, message):
        for remote_client in self.remote_clients:
            remote_client.say(message)
            # if len(message) >= 4:
            #print "request"

    def all_close(self):
        self.remote_clients = []


def dump_dictionary(file_name, index):
    global stats, timestamps, attacks, file_count
    # for t in stats[index]:
    # if 'clients' in stats[index][t]:
    # stats[index][t]['reports'] = len(stats[index][t]['clients'])
    # del stats[index][t]['clients']
    with open(file_name, 'wb') as handle:
        pickle.dump(attacks, handle)
        del attacks
        gc.collect()
        attacks = []

    """
    with open(file_name, 'wb') as handle:
        pickle.dump(stats[index], handle)
        stats[index].clear()
        print "gc = " + str(gc.collect())
    """
    # with open('t-' + file_name, 'wb') as handle:
    # pickle.dump(timestamps[index], handle)


def save_dict(force=False):
    global stats, prev_dict_save, file_count, client_arr, attacks, timestamps, min_timestamp, last_timestamp_recd, save_lock, file_count1
    if not force:
        Timer(10.0, save_dict).start()
    if save_lock:
        return
    save_lock = True
    print len(attacks)
    # print "arr: " + str(len(client_arr))
    if len(attacks) > 500000 or force:
        print "inside"
        # prev_dict_save = int(time.time())
        file_name = "attack-dump-" + str(file_count1) + ".pickle"
        dump_dictionary(file_name, None)
        file_count1 += 1
        # stats.append(defaultdict(dict))
        # stats[file_count].clear()
        # del stats
        # gc.collect()
        # stats = [defaultdict(dict)]
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
    global stats, timestamp_queue, file_count, attacks, dict_dst_count, save_lock
    Timer(5.0, consume_completed_timestamps).start()
    if save_lock:
        return True
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


def consume_time_exceed_timestamps(timestamp):
    global stats, last_timestamp_recd, attacks, DETINT, dict_dst_count, save_lock, backlog_consume
    backlog_consume.append(timestamp)
    if save_lock:
        return True
    print "attacks: " + str(len(attacks)) + " t: " + str(timestamp)
    # if len(attacks) >= 1000000:
    # save_dict(erase=False)
    temp_consume = deepcopy(backlog_consume)
    backlog_consume = []
    for t in temp_consume:
        for dst in stats[t]:
            req_rep = stats[t][dst][0] - stats[t][dst][1]
            if req_rep >= 10:
                attacks.append({"timestamp": t, "dst": dst, "req": stats[t][dst][0], "rep": stats[t][dst][1],
                                "flow_count": req_rep})
        del stats[t]


stats = dict()


def main():
    save_dict()
    # consume_completed_timestamps()
    # consume_time_exceed_timestamps()
    server = Host(address=('localhost', 4242))
    asyncore.loop()


if __name__ == "__main__":
    main()
