import os, sys
import time
import shelve
import numpy
from bitarray import bitarray

FLOWTIMEOUT = 5		# Time in seconds before we consider a flow finished/dead.
DESTSTAT_TIMEOUT = 14400	# Time in minutes before we drop a duration stat we've learned.
DSTRTO = 0.1
PORTRTO = 0.1

# TCP EVENTS (poor-enum: one way)
URG = 0
ACK = 1
PSH = 2
RST = 3
SYN = 4
FIN = 5

class DurationInfo:
  def __init__(self, duration, time_learned, src, saw_syn=True, saw_fin=True, saw_rst=False):
    self.duration = duration
    self.time_learned = time_learned
    self.saw_fin = saw_fin
    self.saw_syn = saw_syn
    self.saw_rst = saw_rst
    self.src = src

class OngoingInfo:
  def __init__(self, time_learned, src, src_port):
    self.time_learned = time_learned
    self.src = src
    self.src_port = src_port

class Destination:
  def __init__(self):
    self.done = {}
    self.ongoing = {}
    self.half_open = {}
    
  def add_finished(self, port, duration, src, saw_syn=True, saw_fin=True, saw_rst=False):
    if port not in self.done:
      self.done[port] = []
    time_learned = int(time.time())
    durationobj = DurationInfo(duration, time_learned, src, saw_syn, saw_fin, saw_rst)
    self.done[port].append(durationobj)
  
  def add_ongoing(self, port, src, src_port, half_open=False):
    time_learned = int(time.time())
    obj = OngoingInfo(time_learned, src, src_port)
    if half_open:
      if port not in self.half_open:
        self.half_open[port] = []
      self.half_open[port].append(obj)
    else:	
      if port not in self.ongoing:
        self.ongoing[port] = []
      self.ongoing[port].append(obj)
    
class DestStorage:
  def __init__(self, filename):
    self.filename = filename
    self.db = {}()

  def add_destination(self, dest_ip):
    try:
      data = self.db[dest_ip]
    except KeyError:
      self.db[dest_ip] = Destination()
  
  def del_destination(self, dest_ip):
    try:
      del self.db[dest_ip]
    except KeyError:
      pass
  
  def add_duration(self, dest_ip, port, duration, src, saw_syn=True, saw_fin=True, saw_rst=False):
    self.add_destination(dest_ip)
    data = self.db[dest_ip]
    data.add_finished(port, duration, src, saw_syn, saw_fin, saw_rst)
    self.db[dest_ip] = data
  
  def add_ongoing(self, dest_ip, port, src, src_port, half_open=False):
    self.add_destination(dest_ip)
    data = self.db[dest_ip]
    data.add_ongoing(port, src, src_port, half_open)
    self.db[dest_ip] = data
  
  def get_dest_info(self, dest_ip):
    try:
      data = self.db[dest_ip]
    except KeyError:
      return None
    return data

  def print_stats(self, flowstorage, label, outfile, dstrto=DSTRTO, portrto=PORTRTO):
    flows = flowstorage.getflows()
    printdests = {}()
    printports = {}()

    # First check if we should print stats per dst and per port or not
    deststats = {}()
    portstats = {}()
    total = 0
    for dst in flows:
      tdst = 0;
      for dport in flows[dst]:
        tport = 0
        for src in flows[dst][dport]:
          for sport in flows[dst][dport][src]:
            flow = flows[dst][dport][src][sport]
            total = total + flow.bytes
            tport = tport + flow.bytes
            tdst = tdst + flow.bytes
        if dst not in portstats:
          portstats[dst] = {}()
        portstats[dst][dport] = tport
      deststats[dst] = tdst

    f = open('stats', 'a')
    # Print only for dests that have more than dstrto
    for dst in deststats:
      f.write(str(dst) + ", " + str(deststats[dst]) + "\n")

      if float(deststats[dst])/float(total) >= 0.1:
        printdests[dst] = 1
        printports[dst] = {}()

    f.close()

    # Print only ports that have more than portrto
    for dst in portstats:
      if dst in printdests:
        for port in portstats[dst]:
          if float(portstats[dst][port])/float(deststats[dst]) >= 0.001:
            printports[dst][port] = 1


    for dst in printdests:
      print "\n******* DESTINATION %s PROTO %s *******\n" % (dst,label)
      print "Total bytes\t%d\n" % deststats[dst]
      for dport in printports[dst]:
        if dport is None:
          continue
        print "\n******* DESTINATION %s PORT %s PROTO %s *******\n" % (dst, dport, label)
        complete = 0
        half_open = 0
        reset = 0
        ongoing = 0
        other = 0
        durations = []

        for src in flows[dst][dport]:
          for sport in flows[dst][dport][src]:
            flow = flows[dst][dport][src][sport]
            if label == "TCP":
              saw_fin = False
              saw_rst = False
              saw_syn = False
              saw_psh = False
              saw_ack = False
              saw_data = False

              if flow.flags_dst2src[SYN] or flow.flags_src2dst[SYN]:
                saw_syn = True
              if flow.flags_dst2src[FIN] or flow.flags_src2dst[FIN]:
                saw_fin = True
              if flow.flags_dst2src[RST] or flow.flags_src2dst[RST]:
                saw_rst = True
              if (flow.flags_dst2src[PSH]) or (flow.flags_src2dst[PSH]):
                saw_data = True
              if (flow.flags_dst2src[ACK]) or (flow.flags_src2dst[ACK]):
                saw_ack = True

              state = ''
              if saw_syn and saw_ack and saw_data and not saw_fin:
                ongoing = ongoing + 1
                state='ON'
              elif saw_syn and not (saw_data and saw_ack) and not saw_fin and not saw_rst:
                half_open = half_open + 1
                state='HALF'
              elif saw_fin:
                complete = complete + 1
                state='COM'
                duration = 1000*(flow.last_packet_seen - flow.first_packet_seen)
                durations.append(duration)
              elif saw_rst:
                reset = reset + 1
                state = 'RST'
              else:
                other = other + 1
                state = 'OTH'
              flows[dst][dport][src][sport].state = state
            else:
              other+=1
        if label == "TCP":
          print "Connections healthy, complete\t%d\nConnections with SYN only\t%d\nConnections ended in RST\t%d\nConnections in progress\t\t%d\nOther connections\t\t%d\n" % (complete, half_open, reset, ongoing, other)
          buf = ""
          if (len(durations) > 0):
            print("Stats on %d completed connections" %(len(durations)))
            x, y = self.cdf(numpy.asarray(durations), numbins=min(len(durations),10))
            print("CDF of durations (dur,cdf):")
            for i,j in zip(x,y):
              temp = "%.2f:%.2f " % (i,j)
              buf = buf + temp
              print("%.2f:%.2f ms" % (i,j))
            print("\n")
          print >>outfile, "DST %s %s %s %s %s %s %s %s %s" % (dst, dport, label, complete, half_open, reset, ongoing, other, buf)
        else:
          print "Total number of connections\t%d" % (other)

    for dst in flows:
      for dport in flows[dst]:
        for src in flows[dst][dport]:
          for sport in flows[dst][dport][src]:
            flow = flows[dst][dport][src][sport]
            print >>outfile, "FLOW %s %s %s %s %s %s %s %s %s %s" % (label, src, sport, dst, dport, flow.flags_src2dst, flow.flags_dst2src, flow.packets, flow.bytes, flow.state)
  
  def update_dest_info(self, flows, most_recent_ts, flow_timeout=FLOWTIMEOUT, dest_stat_timeout=DESTSTAT_TIMEOUT, do_stats=True, clean_old_flows=True):
    # XXXX First, we drop all we know about ongoing and half open - if a connection is still
    # half-open/continuing from last time, we don't want to count it twice.
    # If a half-open or continuing connection has progressed, we don't want to count it twice.
    for dst in self.db:
      tmp = self.db[dst]
      tmp.ongoing = {}
      tmp.halfopen = {}
      self.db[dst] = tmp
    
    flow_db = flows.return_db()

    for flow in flow_db:
      #print("."),
      sys.stdout.flush() 
      flow_dst_full = flow.split('x')[1]
      flow_dst = flow_dst_full.split('-')[0]
      flow_dst_port = flow_dst_full.split('-')[1]
      flow_src_full = flow.split('x')[0]
      flow_src = flow_src_full.split('-')[0]
      flow_src_port = flow_src_full.split('-')[1]
      
      # New dest we have no info on.
      if self.get_dest_info(flow_dst) == None:
        self.add_destination(flow_dst)     
      
      dst_info = self.db[flow_dst]
      flowinfo = flow_db[flow]
  
      # Has this flow ended ?
      saw_fin = False
      saw_rst = False
      saw_syn = False
      saw_dataack = False
      flow_timed_out = False
      num_flows = flows.num_flows
      if flowinfo.flags_dst2src[SYN] or flowinfo.flags_src2dst[SYN]:
        saw_syn = True
      if flowinfo.flags_dst2src[FIN] or flowinfo.flags_src2dst[FIN]:
        saw_fin = True
      if flowinfo.flags_dst2src[RST] or flowinfo.flags_src2dst[RST]:
        saw_rst = True
      if (flowinfo.flags_dst2src[ACK] and flowinfo.flags_dst2src[PSH]) or (flowinfo.flags_src2dst[ACK] and flowinfo.flags_src2dst[PSH]):
        saw_dataack = True
      if flowinfo.last_packet_seen < (most_recent_ts - flow_timeout):
        flow_timed_out = True
      duration = 1000*(flowinfo.last_packet_seen - flowinfo.first_packet_seen)      
  
  def cdf(self, values, numbins=10):
    v = numpy.sort(values) 
    counts, bins = numpy.histogram(v, bins=numbins, normed=True)
    step = len(v)/numbins
    x = []
    y = []
    j = 1
    s = 1
    dx = 0
    for value in v:
      j = j + 1
      if j == step:
        dx = 1*s/float(numbins)
        x.append(dx)
        y.append(value)
        j = 0
        s = s+1
    if dx != 1:
      x.append(1)
      y.append(value)
    return x, y
       
        
class Flow:
  def __init__(self):
    self.first_packet_seen = -1
    self.last_packet_seen = -1
    self.packets = 0
    self.bytes = 0
    self.flags_src2dst = bitarray(6)
    self.flags_src2dst.setall(False)
    self.flags_dst2src = bitarray(6)
    self.flags_dst2src.setall(False)
    self.state = ''

class FlowStorage:
  def __init__(self, filename):
    self.filename = filename
    self.num_flows = 0
    self.flows = {}()

  def flow_count(self):
    return self.num_flows
  
  def getflows(self):
    return self.flows

  def add_flow_event(self, ts, src, sport, dst, dport, event, numbytes, packets):
    flows = self.flows;
    direction=0;
    ip1=src
    ip2=dst
    port1=sport
    port2=dport
    if dst not in flows and src in flows:
      ip1=dst
      ip2=src
      port1=dport
      port2=sport
      direction=1;
    if ip2 not in flows:
      flows[ip2] = {}()
      flows[ip2][port2] = {}()
      flows[ip2][port2][ip1] = {}()
      flows[ip2][port2][ip1][port1] = Flow()
    elif port2 not in flows[ip2]:
      flows[ip2][port2] = {}()
      flows[ip2][port2][ip1] = {}()
      flows[ip2][port2][ip1][port1] = Flow()
    elif ip1 not in flows[ip2][port2]:
      flows[ip2][port2][ip1] = {}()
      flows[ip2][port2][ip1][port1] = Flow()
    elif port1 not in flows[ip2][port2][ip1]:
      flows[ip2][port2][ip1][port1] = Flow() 
    flow = flows[ip2][port2][ip1][port1]
    if (flow.first_packet_seen == -1):
      self.num_flows = self.num_flows + 1
      flow.first_packet_seen = ts
      flow.flags_src2dst.setall(False)
      flow.flags_dst2src.setall(False)
    
    flow.last_packet_seen = ts
    # Set the right array bits.
    # Figure out which direction this came from.
    if event is not None and event !=6:
      if direction == 0:
        flow.flags_src2dst |= bitarray(event)
      else:
        flow.flags_dst2src |= bitarray(event)
      
    flow.packets = flow.packets + packets
    flow.bytes = flow.bytes + numbytes
    # Put in new flow data or overwrite old flow info with new update.  
    flows[ip2][port2][ip1][port1] = flow

       
  def flow_in_storage(self, flow_key):
    try:	
      data = self.db[flow_key]
      key = flow_key
    except KeyError:
      # We may have flipped src and dst. Check both ways.
      flipkey = flow_key.split('x')[1] + 'x' + flow_key.split('x')[0]
      try:
        data = self.db[flipkey]
        key = flipkey
      except KeyError:
        key = None
    return key
  
  def get_flow_info(self, flow_key):
    try:
      data = self.db[flow_key]
    except KeyError:
      return None
    return data
  
  """
  Before calling, a snapshot of what we know about destinations should be created,
  so the info we've collected isn't a wasted effort.
  """
  def clear_old_flow(self, flow_key):
    flowinfo = self.db[flow_key]
    self.num_flows = self.num_flows - 1
    del self.db[flow_key]

  
