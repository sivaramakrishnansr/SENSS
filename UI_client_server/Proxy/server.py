
'''
Packet sniffer in python using the pcapy python library
 
Project website
http://oss.coresecurity.com/projects/pcapy.html
'''
 
import socket
from struct import *
import datetime
import pcapy
import sys
import time 
counter=0
def main(argv):
    #list all devices
    devices = pcapy.findalldevs()
    print devices
     
    #ask user to enter device name to sniff
    cap = pcapy.open_live("eth4" , 65536 , 1 , 0)
    global counter
    #start sniffing packets
    s=time.time()
    while(1) :
	try:
        	(header, packet) = cap.next()
	except:
		continue
	if time.time()-s>=5:
		print counter
		if counter<=2:
			print "Failed to get messages"
			fw=open("proxy_file","w")
			fw.write("yes")
			fw.close()
		else:
			print "Got sufficient messages"
			fw=open("proxy_file","w")
			fw.write("no")
			fw.close()
		
		counter=0
		s=time.time()

        #print ('%s: captured %d bytes, truncated to %d bytes' %(datetime.datetime.now(), header.getlen(), header.getcaplen()))
        parse_packet(packet)
 	
#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
    return b
 
#function to parse a packet
def parse_packet(packet) :
    #parse ethernet header
    eth_length = 14
    global counter
    eth_header = packet[:eth_length]
    eth = unpack('!6s6sH' , eth_header)
    eth_protocol = socket.ntohs(eth[2])
    if eth_protocol == 8 :
        ip_header = packet[eth_length:20+eth_length]
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        ttl = iph[5]
        protocol = iph[6]
	#if protocol==1:
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
 	if d_addr=="48.0.0.1":
 		counter=counter+1
		#print protocol,d_addr,counter
		
if __name__ == "__main__":
  main(sys.argv)

