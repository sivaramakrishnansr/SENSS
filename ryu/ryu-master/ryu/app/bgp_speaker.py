import eventlet
import json
eventlet.monkey_patch()

import logging
import sys
log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker

if __name__ == "__main__":
    speaker = BGPSpeaker(as_number=10, router_id='10.0.0.1',
                         ssh_console=True)


    speaker.neighbor_add('10.9.10.1', 9)
    speaker.neighbor_add('10.5.10.1', 5)
    prefix = '10.0.0.0/8'
    print "add a new prefix", prefix
    speaker.prefix_add(prefix)


    while True:
        eventlet.sleep(5)





'''
import eventlet

# BGPSpeaker needs sockets patched
eventlet.monkey_patch()

# initialize a log handler
# this is not strictly necessary but useful if you get messages like:
#    No handlers could be found for logger "ryu.lib.hub"

import logging
import sys
log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stderr))

from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker

def dump_remote_best_path_change(event):
    print 'the best path changed:', event.remote_as, event.prefix,\
        event.nexthop, event.is_withdraw

def detect_peer_down(remote_ip, remote_as):
    print 'Peer down:', remote_ip, remote_as

if __name__ == "__main__":
    speaker = BGPSpeaker(as_number=10,router_id='10.0.0.1',
                         best_path_change_handler=dump_remote_best_path_change,
                         peer_down_handler=detect_peer_down)


    speaker.neighbor_add('10.2.10.1', 2)
    speaker.neighbor_add('10.9.10.1', 9)
    speaker.neighbor_add('10.8.10.1', 8)
    speaker.neighbor_add('10.5.10.1', 5)

    # uncomment the below line if the speaker needs to talk with a bmp server.
    # speaker.bmp_server_add('192.168.177.2', 11019)
    count = 1
    while True:
        eventlet.sleep(30)
        #prefix = '10.0.' + str(count) + '.0/24'
        prefix = '10.0.0.0/24'
        print "add a new prefix", prefix
        speaker.prefix_add(prefix)
	break
        count += 1
        if count == 4:
            speaker.shutdown()
            break
'''
