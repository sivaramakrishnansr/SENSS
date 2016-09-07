import signal
import sys
import argparse
import ipaddress
from stats import *
import re
import operator

TCP=0
UDP=1
ICMP=2

tlabel = ['TCP','UDP','ICMP']

def deal_with_arguments():
  parser = argparse.ArgumentParser(description='Detects attack and suggests fields that can be used for filtering. Assumes baseline and attack files were collected with the same interval.')
  parser.add_argument('--base', '--base', dest='baseline', default='/tmp/baseline.fs', help="Name of database file for baseline statistics. Default '/tmp/baseline'")
  parser.add_argument('--current', '--current', dest='current', default='/tmp/current.fs', help="Name of database file for current statistics. Default '/tmp/current'")

  args = parser.parse_args()
  return args

def signal_handler(signal, frame):
  sys.exit(0)


def main():
  signal.signal(signal.SIGINT, signal_handler)
  args = deal_with_arguments()

  params = dict()

  c = open('detect.conf', 'r')
  conf = c.read()
  for l in conf.split("\n"):
    items = l.split(" ")
    params[items[0]] = float(items[1])
  
  try:
    base = open(args.baseline, 'r')
    #baseline = base.read()
  except Exception as e:
    print "Problem reading file %s:\n\t%s" % (args.baseline,e)  
    exit()
  try:
    cur = open(args.current, 'r')
    #current = cur.read()
  except Exception as e:
    print "Problem reading file %s:\n\t%s" % (args.current,e)  
    exit()

  #blines = baseline.split("\n")
  for b in base.xreadlines():
    al = re.compile('ALL')
    dst = re.compile('DST')
    flow = re.compile('FLOW')
    if al.match(b):
      first = Stats(b)
    elif dst.match(b):
      first.add_dst(b)
    elif flow.match(b):
      first.add_flow(b)

  #clines = current.split("\n")
  for c in cur.xreadlines():
    al = re.compile('ALL')
    dst = re.compile('DST')
    flow = re.compile('FLOW')
    if al.match(c):
      second = Stats(c)
    elif dst.match(c):
      second.add_dst(c)
    elif flow.match(c):
      second.add_flow(c)

  # Can we filter on dst, dport or their combination?
  firststats = dict()
  firststats['src'] = dict()
  firststats['dst'] = dict()
  firststats['ho'] = dict()

  for dst in first.flows:
    if dst not in firststats['dst']:
      firststats['dst'][dst] = dict()
    tdst = 0 # This stores sum of bytes sent from all sports of all srcs to all dports of dst
    for dport in first.flows[dst]:
      tdport = 0 # This stores sum of bytes sent from sport of src to dport of dst
      for src in first.flows[dst][dport]:
        if src not in firststats['src']:
          firststats['src'][src] = dict()
        for sport in first.flows[dst][dport][src]:
          flow = first.flows[dst][dport][src][sport]
          tdport = tdport + flow.bytes
          tdst = tdst + flow.bytes
          if sport not in firststats['src'][src]:
            firststats['src'][src][sport] = 0
          firststats['src'][src][sport] = firststats['src'][src][sport] + flow.bytes #Bytes sent from sport of src to dport of dst
          if (flow.state.strip() == 'HALF'):
            if src not in firststats['ho']:
              firststats['ho'][src] = dict()
            if sport not in firststats['ho'][src]:
              firststats['ho'][src][sport] = 0
            firststats['ho'][src][sport] = firststats['ho'][src][sport] + flow.bytes
        firststats['dst'][dst][dport] = tdport # Total bytes sent to dport at dst from all ports of all sources with flows to dst


  secondstats = dict()
  secondstats['src'] = dict()
  secondstats['dst'] = dict()
  # Half-open same as src but just for half-open conns
  secondstats['ho'] = dict()

  for dst in second.flows:
    if dst not in secondstats['dst']:
      secondstats['dst'][dst] = dict()
    tdst = 0
    for dport in second.flows[dst]:
      tdport = 0
      for src in second.flows[dst][dport]:
        if src not in secondstats['src']:
          secondstats['src'][src] = dict()
        for sport in second.flows[dst][dport][src]:
          flow = second.flows[dst][dport][src][sport]
          tdport = tdport + flow.bytes
          tdst = tdst + flow.bytes
          if sport not in secondstats['src'][src]:
            secondstats['src'][src][sport] = 0
          secondstats['src'][src][sport] = secondstats['src'][src][sport] + flow.bytes
          if (flow.state.strip() == 'HALF'):
            if src not in secondstats['ho']:
              secondstats['ho'][src] = dict()
            if sport not in secondstats['ho'][src]:
              secondstats['ho'][src][sport] = 0
            secondstats['ho'][src][sport] = secondstats['ho'][src][sport] + flow.bytes
        secondstats['dst'][dst][dport] = tdport



  detected = 0
  syn_flood = 0
  ermsg = ""
  for d in first.dsts:
    ips=[]
    for p in first.dsts[d]:
      ips.append(first.flows[d][p].keys())

      if d not in second.dsts:  #A
        detected = 1
        ermsg += "You have no traffic to dest %s" % d
      elif p not in second.dsts[d]:
        detected = 1
        ermsg += "You have no traffic to dest %s port %s" % (d,p)
      if (second.dsts[d][p].halfopen > params['THRESH_COMPLETE']*first.dsts[d][p].halfopen and first.dsts[d][p].halfopen > 0)\
              or (first.dsts[d][p].halfopen == 0 and second.dsts[d][p].complete !=0 and second.dsts[d][p].halfopen/second.dsts[d][p].complete > 0.5):
        detected = 1
        syn_flood = 1
        ermsg += "You have many half open connections to dest %s port %s increased from %s to %s, possibility of a SYN Flood; " % (d,p,first.dsts[d][p].halfopen,second.dsts[d][p].halfopen)

      print "DST %s:%s" % (d,p) #B
      print "Original complete connections %s now %s" % (first.dsts[d][p].complete,second.dsts[d][p].complete)
      orig = first.dsts[d][p].getavg()
      cur = second.dsts[d][p].getavg()
      print "Original connection duration %s ms now %s ms" % (orig, cur)

      if second.dsts[d][p].complete < params['THRESH_COMPLETE']*first.dsts[d][p].complete:
        detected = 1
        ermsg += "Destination %s:%s has too few complete connections, reduced from %s to %s\n" % (d, p, first.dsts[d][p].complete, second.dsts[d][p].complete)
      elif cur > 10*orig:
        detected = 1
        ermsg += "Destination %s:%s has too long connections, average increased from %.2f to %.2f ms\n" % (d, p, orig, cur)
      elif cur > params['THRESH_DUR']*orig and d in secondstats['ho'] and len(secondstats['ho'][d][p])/second.dsts[d][p] > 0.1:
        detected = 1
        ermsg += "Destination %s:%s has longer connections and unanswered SYNs" % (d, p)

    if d in ips:
      detected = 1
      ermsg += "Packets found with same destination and source IPs %s, possible LAND attack" % (d)

  if not detected:
    print "NO ATTACK DETECTED\n"
  else:
    print "ATTACK DETECTED\n%s" % ermsg
    print "FILTER SUGGESTIONS\n"
    suggestions = dict()
    ototal = 0
    total = 0
    for i in range(0,3):
      total = total + second.bytes[i] #Bytes of TCP, UDP & ICMP respectively in current fs
      ototal = ototal + first.bytes[i] #Bytes of TCP, UDP & ICMP respectively in base fs

    # Can we filter on traffic type? - This checks whether the percentage of each traffic type (TCP/UDP/ICMP) is greater than some threshold value/relative to base file

    for i in range(0,3):
      if (first.bytes[i] != 0 and second.bytes[i] > params['THRESH_TRAF_RELATIVE']*first.bytes[i]): # 2 times the base fs file protocol bytes
        suggestions['proto ' + tlabel[i]] = Filter("0.0.0.0\t",0,tlabel[i], float(second.bytes[i])/total, float(first.bytes[i])/ototal, 'proto ' + tlabel[i])
      elif (first.bytes[i] == 0 and second.bytes[i]/ototal > params['THRESH_TRAF_ABSOLUTE']):
        suggestions['proto ' + tlabel[i]] = Filter("0.0.0.0\t",0,tlabel[i], float(second.bytes[i])/total, float(first.bytes[i])/ototal, 'proto ' + tlabel[i])
      used = float(second.bytes[i])*8/10/1000000000
      desired = params['THRESH_TRAF_ABSOLUTE']*params['CAPACITY']
      if used > desired: #This covers the bandwidth of a link and its usage by a protocol
        if (('proto '+tlabel[i]) not in suggestions):
          suggestions['proto '+tlabel[i]] = Filter("0.0.0.0\t",0,tlabel[i], float(second.bytes[i])/total, float(first.bytes[i])/ototal, 'proto '+tlabel[i])

    # First try dest/dport or src/sport combination if possible. 
    # Pick top ones by bytes sent/received according to THRESH_FILTER value

    for label in ('src','dst', 'ho'):
      values = []
      if label == 'ho' and syn_flood==1:
        half_open = dict()
        for ip in secondstats[label]:
          half_open[ip] = 0
          for port in secondstats[label][ip]:
            half_open[ip] +=1
            if(half_open[ip] > 50):
              if ip in firststats[label]:
                fvalue = len(firststats[label][ip])
              suggestions[label + ' ' + ip + ":0"] = Filter(ip, 0,"", half_open[ip], fvalue, label)
        break;


      for a in secondstats[label]: #for each IP in src,dest,ho
        for b in secondstats[label][a]: #for each port in IP
          values.append(FD(a, b, secondstats[label][a][b])) #add number of bytes on that port to values list

      values.sort(key=lambda x: x.value, reverse=True) #Sort on number of bytes - Can have max values list while collecting stats above

      i = 1
      for v in values:
        if a not in firststats[label]:
          fvalue = 0
        elif b not in firststats[label][a]:
          fvalue = 0
        else:
          fvalue = float(firststats[label][a][b])
        suggestions[label + ' ' + v.ip + ":" + v.port] = Filter(v.ip, v.port,"", float(v.value)/total, float(fvalue)/ototal, label + 'port')
        i = i + 1
        if i >= params['THRESH_FILTER']:
          break
          

    # Next try just src or dst or half-open and look for sources that send a lot
    for label in ('src','dst','ho'):
      ips = dict()
      values = []
      for a in secondstats[label]:
        sum = 0
        for b in secondstats[label][a]:
          sum = sum + secondstats[label][a][b]
        values.append(FD(a, 0, sum))
        if a in firststats[label]:
          sum = 0
          for b in firststats[label][a]:
            sum = sum + firststats[label][a][b]
        else:
          sum = 0
        ips[a] = sum

      values.sort(key=lambda x: x.value, reverse=True)

      i = 1
      for v in values:
        suggestions[label + ' ' + v.ip + ":0"] = Filter(v.ip, 0,"", float(v.value)/total, float(ips[v.ip])/ototal, label)
        i = i + 1
        if i >= params['THRESH_FILTER']:
          break

    # Next try to find a port that sends a lot
    for label in ('src','dst', 'ho'):
      ports = dict()
      values = []
      for a in secondstats[label]:
        for b in secondstats[label][a]:
          if b not in ports:
            ports[b] = 0
          ports[b] = ports[b] + secondstats[label][a][b]
      for b in ports:
        values.append(FD(0, b, ports[b]))
      ports = dict()
      for a in firststats[label]:
        for b in firststats[label][a]:
          if b not in ports:
            ports[b] = 0
          ports[b] = ports[b] + firststats[label][a][b]

      values.sort(key=lambda x: x.value, reverse=True)
      i = 1
      for v in values:
        if v.port not in ports:
          ports[v.port] = 0
        suggestions[label + ' 0:'+v.port] = Filter("0.0.0.0\t", v.port, "", float(v.value)/total, float(ports[v.port])/ototal, label)
        i = i + 1
        if i >= params['THRESH_FILTER']:
          break

    filters=suggestions.values()
    filters.sort(key=lambda x: (float(x.tp)-float(x.fp)), reverse = True)
    
    print "Num\tIP\tport\tproto\tfiltered\tcollateral\ttype"
    print "****************************************************************\n"
    i = 0
    for s in filters:
      i = i+1
      proto='any'
      type='any'
      if (s.reason.startswith("proto")):
        proto = s.reason[6:].lower()
      elif(s.reason.startswith("src")):
        type='src'
      elif(s.reason.startswith("ho")):
        type='src'
      else:
        type='dst'


      tp = "%.2f" % (s.tp*100)
      fp = "%.2f" % (s.fp*100)


      print "%d\t%s\t%s\t%s\t%s\t%s\t%s" % (i, s.ip, s.port, proto, tp, fp, type)
      

if __name__ == "__main__":
  main()
