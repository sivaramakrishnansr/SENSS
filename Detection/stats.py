import os, sys
import time
import numpy
from bitarray import bitarray

class Stats:
  def __init__(self, string):
    items = string.split(" ")
    self.packets = dict()
    for i in range (0,3):
      self.packets[i] = int(items[i+1])
    self.bytes = dict()
    for i in range (3,6):
      self.bytes[i-3] = int(items[i+1])
    self.dsts = dict()
    self.flows = dict()
      
  def add_dst(self, string):
    items = string.split(" ")
    ip = items[1]
    port = items[2]
    if ip not in self.dsts:
      self.dsts[ip] = dict()
    cdf = dict()
    for i in range(9, len(items)-1):
      parts = items[i].split(":")
      cdf[parts[0]] = parts[1]
    self.dsts[ip][port] = Dest(items[3],items[4], items[5], items[6], items[7], items[8], cdf)

  def add_flow(self, string):
    items = string.split(" ")
    proto = items[1].lower()
    src = items[2]
    sport = items[3]
    dst = items[4]
    dport = items[5]
    if dst not in self.flows:
      self.flows[dst] = dict()
    if dport not in self.flows[dst]:
      self.flows[dst][dport] = dict()
    if src not in self.flows[dst][dport]:
      self.flows[dst][dport][src] = dict()
    self.flows[dst][dport][src][sport] = Flow(proto, items[8], items[9], items[10])

    
    
class Dest:
  def __init__(self, proto, complete, halfopen, reset, ongoing, other, cdf):
    self.proto = proto
    self.complete = int(complete)
    self.halfopen = int(halfopen)
    self.reset = int(reset)
    self.ongoing = int(ongoing)
    self.other = int(other)
    self.cdf = cdf

  def getavg(self):
    sum = 0
    px = 0
    pv = 0
    for c in self.cdf:
      sum = sum + float(self.cdf[c])
    l = len(self.cdf)
    if l == 0:
      l = 1
    sum = sum / float(l)
    return sum

class Flow:
  def __init__(self, proto, packets, bytes, state):
    self.proto = proto
    self.packets = int(packets)
    self.bytes = int(bytes)
    self.state = state
    self.state.strip()

class Filter:
  def __init__(self, ip, port, proto, tp, fp, reason):
    self.ip = ip
    self.port = port
    self.proto = proto
    self.tp = tp
    self.fp = fp
    self.reason = reason


class FD:
  def __init__(self, ip, port, value):
    self.ip = ip
    self.port = port
    self.value = value

    
