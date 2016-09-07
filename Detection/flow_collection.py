import signal
import sys
import plt
import argparse
import ipaddress
from flow_storage import *
  
def deal_with_arguments():
  parser = argparse.ArgumentParser(description='Summerizes flows from a device or trace.')
  parser.add_argument('-i', '--interval', dest='interval', default=60, type=int, help='Interval in seconds to print/calculate stats over (seconds based on input Trace URI).')
  parser.add_argument('-d', '--target', dest='target', default=None, help='Focus on a specific target IP or target net.')
  parser.add_argument('-b', '--bpf', dest='filter', default=None, help="BPF style filter to apply.")
  parser.add_argument('--flowdb', '--fdb', dest='flow_db_name', default='/tmp/flowdb', help="Name of database file for flow info. Default '/tmp/flowdb'")
  parser.add_argument('--destdb', '--ddb', dest='dest_db_name', default='/tmp/destdb', help="Name of database file for destination summary info. Default '/tmp/destdb'")
  parser.add_argument('-p', '--keep_dbs', dest='storage', action='store_true', default=False, help="Keep databases around after program finishes.")
  parser.add_argument('input', nargs=1, help="Trace URI (eg. 'int:eth0' or 'pcapfile:./trace.dump') If no type given, assumed to be pcapfile.")

  args = parser.parse_args()
  if ':' not in  args.input[0]:
    print("No type for input given. Assuming pcap file.")
    args.input = 'pcapfile:' + args.input[0]
  else:
    args.input = args.input[0]
  return args

def signal_handler(signal, frame):
  sys.exit(0)


def main():
  signal.signal(signal.SIGINT, signal_handler)
  args = deal_with_arguments()
  
  # Set up our storage.
  try:
    flows = FlowStorage(filename=args.flow_db_name, persistant_storage=args.storage)
    dests = DestStorage(filename=args.dest_db_name, persistant_storage=args.storage)
  except Exception as e:
    print("Problem setting up databases:\n\t%s" % e)  
    exit()

  # Try opening our trace.
  try:
    t = plt.trace(args.input)
  except Exception as e:
    print("Trouble opening trace URI/device:\n\t%s" % e)
    exit()
    
  # Try setting up our filter if given one.
  try:
    if args.filter != None or args.target != None:
      if args.filter != None and args.target != None:
          args.filter = args.filter + " and "
      elif args.filter == None:
        args.filter = ""
      if args.target != None:
        args.filter = args.filter + "dst "
        if '/' in args.target:
          args.filter = args.filter + "net "
        args.filter = args.filter + args.target
      f = plt.filter(args.filter)
      print("Applying filter \"%s\"" % args.filter)
      t.conf_filter(f)
  except Exception as e:
    print("Trouble applying bpf filter: \'%s\'\n\t%s"% (args.filter,e))
    exit()
    
  print("Press Ctrl+C to exit.")

  # Try reading.
  try:
    t.start()
  except Exception as e:
    print(e)
    exit()
  
  # And we're off - loop for as long as we get packets (or ^C)
  packet_count = 0
  non_ipv4_packets = 0
  non_ip_packets = 0
  non_tcp_packets = 0
  last_time_check_pkt_ts = 0
  current_time = int(time.time())
  do_stats_time = current_time + args.interval
  do_updates_time = current_time + 15
  last_packet_count = 0
  last_ts = -2
  current_ts = -1

  print("Packets processed:\t"),
  for pkt in t:	
    packet_count = packet_count + 1
    last_packet_count = last_packet_count + 1
    last_ts = current_ts
    current_ts = pkt.seconds
    
    if last_ts > (current_ts + .5):
      print("PROBLEM: timestamps out of order: Last ts: %f this ts: %f" %(last_ts, current_ts))
      exit()
    
    print("%012d\b\b\b\b\b\b\b\b\b\b\b\b" % packet_count),
    
    # If we've gone through an interval's worth of packets, check the actual time
    # we may be going through packets *much* faster than real-time if we're
    # reading from a trace, but this keeps us from constantly checking the time
    # to determine when we update/print stats.
    if current_ts - last_time_check_pkt_ts > 3 or last_packet_count > 100:
      current_time = int(time.time())
      last_time_check_pkt_ts = current_ts 
      if do_stats_time < current_time:
        print("\nDo stats")
        dests.update_dest_info(flows, current_ts)
        do_stats_time = current_time + args.interval
        do_update_time = current_time + 60
        print("Packets processed:\t"),
      elif do_updates_time < current_time or last_packet_count > 100:
        print("\nUpdating tables %d" % last_packet_count)
        last_packet_count = 0
        dests.update_dest_info(flows, current_ts, do_stats=False)
        do_updates_time = current_time + 60
        print("Packets processed:\t"),
        
    # IP layer
    ip = pkt.ip    
    if not ip:
      non_ip_packets = non_ip_packets+1 
      continue
    
    # IPv4
    if ip.version != 4:
      non_ipv4_packets = non_ipv4_packets + 1
      continue
    
    # TCP is al we care about right now.
    tcp = pkt.tcp
    if not tcp:
      non_tcp_packets = non_tcp_packets + 1
      continue
    
    # Get what we're using for dictionary keys.
    pkt_src = str(ip.src_prefix)
    pkt_dst = str(ip.dst_prefix)
    pkt_sport = str(tcp.src_port)
    pkt_dport = str(tcp.dst_port)
    
    # Not perfect - we don't check for certain combinations (ie combinations that don't make sense).
    event = OTHER
    if tcp.syn_flag:
      if not tcp.ack_flag:
        event = SYN
      else:
        event = SYN_ACK
    elif tcp.fin_flag:
      event = FIN
    elif tcp.rst_flag:
      event = RST
    elif tcp.ack_flag or tcp.urg_flag or tcp.psh_flag:
      event=ACK_AND_DATA
    else:
      print("Unknown flags!")
      
    # Ready to store.
    flows.add_tcp_flow_event(current_ts, pkt_src, pkt_sport, pkt_dst, pkt_dport, event)
  
  print("\nDone\n")
  dests.update_dest_info(flows, current_ts+DESTSTAT_TIMEOUT)
  
  flows.close()
  dests.close()
    
if __name__ == "__main__":
  main()
  dests = Destination()  
