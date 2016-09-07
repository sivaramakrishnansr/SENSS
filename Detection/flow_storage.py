
import os, sys
import time
import shelve
import numpy
from bitarray import bitarray

FLOWTIMEOUT = 5		# Time in seconds before we consider a flow finished/dead.
DESTSTAT_TIMEOUT = 14400	# Time in minutes before we drop a duration stat we've learned.

# TCP EVENTS (poor-enum: one way)
SYN = 0
SYN_ACK = 1
ACK_AND_DATA = 2
FIN = 3
RST = 4
OTHER = 5

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
  def __init__(self, filename='/tmp/dsts', persistant_storage=False):	
    self.persistant = persistant_storage
    # Check if file exists, and if it does, test if this database makes sense.
    if os.path.isfile(filename):
      try:
        self.db = shelve.open(filename)
        anykey = self.db.iterkeys().next()
        tmp = self.db[anykey]
        if not isinstance(tmp.done, dict):
          raise ValueError("Not given valid database.")
      except:
        print("%s exists and does not appear to be a valid database for this program." % filename)
        raise
    else:
      self.db = shelve.open(filename)
    if not persistant_storage:
      self.db.clear()
  
  def close(self):
    self.db.close()
    # Should remove db if not asked to keep persistant storage.   
      
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
      if flowinfo.flags_dst2src[ACK_AND_DATA] or flowinfo.flags_src2dst[ACK_AND_DATA]:
        saw_dataack = True
      if flowinfo.last_packet_seen < (most_recent_ts - flow_timeout):
        flow_timed_out = True
      duration = flowinfo.last_packet_seen - flowinfo.first_packet_seen
      
      if flow_timed_out:
        # We've seen all we should see for this flow - so report!
        self.add_duration(flow_dst, flow_dst_port, duration, flow_src, saw_syn, saw_fin, saw_rst)
        flows.clear_old_flow(flow)
      # Even though these have ended, they have *just* ended, so we may still get an
      # ACK or FIN - so don't report these as done just yet.
      elif saw_fin or saw_rst:
        if not saw_syn and not saw_dataack:
          # We just have a RST or FIN - so not really a connection.
          pass
        elif flowinfo.last_packet_seen < (most_recent_ts - (flow_timeout)):
          self.add_duration(flow_dst, flow_dst_port, duration, flow_src, saw_syn, saw_fin, saw_rst)
          flows.clear_old_flow(flow)   
        else:
          self.add_ongoing(flow_dst, flow_dst_port, flow_src, flow_src_port, half_open=False)
      elif saw_dataack:
        self.add_ongoing(flow_dst, flow_dst_port, flow_src, flow_src_port, half_open=False)
      elif flowinfo.flags_src2dst[SYN] and flowinfo.flags_dst2src[SYN_ACK]:
        self.add_ongoing(flow_dst, flow_dst_port, flow_src, flow_src_port, half_open=True)
      elif saw_syn:
        # XXX May want to log this.
        pass
      else:
        print("Um, what did we see?")
    # Do per dest stats, and clean up old stats.
    if do_stats:
      self.dst_stats(dest_stat_timeout)

  def dst_stats(self, dest_stat_timeout):
    now = int(time.time())
    print("*******************************************************************")
    for dest, data in self.db.iteritems():
      #data = self.db[dest]
      ongoing_ports = data.ongoing.keys()
      half_open_ports = data.half_open.keys()
      done_ports = data.done.keys()
      all_ports = sorted(set(ongoing_ports + half_open_ports + done_ports))
      print("%s: " % (dest))
      for port in all_ports:	
        print("\t %d: " % int(port))
        try:
          print("\t\t On going (progressing): %d" %(len(data.ongoing[port])))
        except KeyError:
          pass
        try:
          print("\t\t Half open: %d" %(len(data.half_open[port])))
        except KeyError:
          pass
        if port in data.done:
          complete_durs = []
          saw_complete = 0
          saw_fin_durs = 0
          clients = []
          rst_durs_count = 0
          timedout = 0
          stat_timeout = 0
          for durobj in data.done[port]:
            if durobj.time_learned >= now - dest_stat_timeout:
              # Info on this connection hasn't timed out.
              clients.append(durobj.src)
              complete_durs.append(durobj.duration)
              if durobj.saw_syn and durobj.saw_fin:
                saw_complete = saw_complete + 1
              elif durobj.saw_rst:	
                rst_durs_count = rst_durs_count + 1
              elif durobj.saw_fin:
                # These are connections we saw the fin for, but not the syn
                saw_fin_durs = saw_fin_durs + 1 
              else:
                # If we didn't see a rst or fin then this flow timed out and was concidered done.
                timedout = timedout + 1    
            else:
              # Connection information has timed out.
              data.done[port].remove(durobj)
          print("\t\t %d connections ended in RST" %(rst_durs_count))
          print("\t\t %d connections ended in FIN (but we missed the SYN)" %(saw_fin_durs))
          print("\t\t %d connections we assume ended (timedout)" %(timedout))
          print("\t\t %d connections we saw SYN and FIN for" %(saw_complete))
          if len(complete_durs) > 4:
            print("\t\t Stats on %d finished connections" %(len(complete_durs)))
            x, y = self.cdf(numpy.asarray(complete_durs), numbins=min(len(complete_durs),10))
            print("\t\tCDF of durations (dur,cdf):")
            print("\t\t"),
            for i,j in zip(x,y): print("%.2fs:%.2f" % (i,j)),
            print("\n")
          else:
            print("\t\t Too few values for CDF. Connection durations:")
            print("\t\t"),
            for i in sorted(complete_durs): print("%.2f s" % float(i)),
            print("\n")
              
      # In case we've deleted durobj
      self.db[dest] = data                                
    print("*******************************************************************")
    print
  
  def cdf(self, values, numbins=10):
    v = numpy.sort(values) 
    counts, bins = numpy.histogram(v, bins=numbins, normed=True)
    dx = bins[1] - bins[0]
    cdf = numpy.cumsum(counts)*dx
    #x,f = numpy.unique(v, return_index=True)
    #cdf = np.array(range(len(v)))/float(len(v))
    last_j = -1
    last_i = -1
    x = []
    y = []
    for i, j in zip(bins[1:], cdf):
      if str("%.2f" % i) == str("%.2f" % last_i):
        if x != [] and y != []:
          x.pop()
          y.pop()
      if j != last_j:
        x.append(i)
        y.append(j)
      last_j = j
      last_i = i
    #return v, cdf
    #return bins[1:], cdf
    return x, y
       
        
class Flow:
  def __init__(self):
    self.first_packet_seen = -1
    self.last_packet_seen = -1
    self.flags_src2dst = bitarray(6)
    self.flags_dst2src = bitarray(6)

class FlowStorage:
  def __init__(self, filename='/tmp/flows', persistant_storage=False):
    self.num_flows = 0
    if os.path.isfile(filename):
      try:
        self.db = shelve.open(filename)
        #anykey = self.db.iterkeys().next()
        #tmp = self.db[anykey]
        #if not hasattr(tmp, 'first_packet_seen'):
        #  raise ValueError("Not given valid database.")
      except:
        print("%s exists and does not appear to be a valid database for this program." % filename)
        raise
    else:
      self.db = shelve.open(filename)
    if not persistant_storage:
      self.db.clear()
  def close(self):
    self.db.close()
    # Should remove db if not asked to keep persistant storage.  
  
  def flow_count(self):
    return self.num_flows
  
  def add_tcp_flow_event(self, ts, event_src, sport, event_dst, dport, event):
    key = self.flow_in_storage(event_src + '-' + sport + 'x' + event_dst + '-' + dport)
    if key == None:
      # New flow
      if event == SYN or (int(dport) > int(sport) and event != SYN_ACK):
          key = event_src + '-' + sport + 'x' + event_dst + '-' + dport
      else:
          key =  event_dst + '-' + dport + 'x' + event_src + '-' + sport
      flow = Flow()
      flow.first_packet_seen = ts
      self.num_flows = self.num_flows + 1
    else:
      # Get copy of flow to modify it.
      flow = self.db[key]
    
    # This event is the last packet we've seen, update timestamp
    flow.last_packet_seen = ts
    
    # Set the right array bits.
    # Figure out which direction this came from.
    flow_src = key.split('x')[0]
    flow_dst = key.split('x')[1]
    if event_src + '-' + sport == flow_src:
      flow.flags_src2dst[event] = True
    if event_src + '-' + sport == flow_dst:
      flow.flags_dst2src[event] = True
    
    # Put in new flow data or overwrite old flow info with new update.  
    self.db[key] = flow
       
  # XXX hack
  def return_db(self):
    return self.db

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

  
