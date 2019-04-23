#!/usr/bin/env python
import time
import os
import pexpect
import subprocess
import sys

#Command line arguments
number_of_ports=1
type=sys.argv[1]
if type=="ddos_with_sig" or type=="proxy" or type=="amon_proxy":
	attack_ip=sys.argv[2]
	attack_duration=int(sys.argv[3])
	attack_rate=sys.argv[4]
	switch_mac=sys.argv[5]
	server_mac=sys.argv[6]
	source_ip=sys.argv[7]
	legit_traffic=int(sys.argv[8])
	legit_traffic_rate=sys.argv[9]
	legit_duration=int(sys.argv[10])
	legit_address=sys.argv[11]

if type=="ddos_without_sig":
	as_name=sys.argv[2].split(".")[0].replace("hpc0","")
	attack_ip=sys.argv[3]
	attack_duration=int(sys.argv[4])
	attack_rate=sys.argv[5]
	switch_mac=sys.argv[6]
	server_mac=sys.argv[7]
	legit_sources=int(sys.argv[8])
	attack_sources=int(sys.argv[9])
	legit_traffic_rate=sys.argv[10]
	legit_duration=int(sys.argv[11])
	legit=2
	legit_traffic_start=as_name+".0.0."+str(legit)
	legit=legit+legit_sources-1
	legit_traffic_end=as_name+".0.0."+str(legit)
	attack=legit+1
	attack=2
	source_ip_start=as_name+".0.0."+str(attack)
	attack=attack+attack_sources
	source_ip_end=as_name+".0.0."+str(attack)
	




proc = subprocess.Popen(["arp"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
out=out.split("\n")
for line in out:
	if len(line.strip())==0:
		continue
	line=line.strip().split()
	interface=line[-1]
	mac_address=line[2]
	if interface=="eth6":
		switch_mac_1=mac_address
	if interface=="eth7":
		switch_mac_2=mac_address

#proc = subprocess.Popen(["ifconfig eth6"], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#out=out.split("\n")
#for line in out:
#	if "HWaddr" in line:
#		server_mac=line.strip().split()[-1]
#	if "inet addr" in line:
#		source_ip=line.strip().split("inet addr:")[-1].split()[0].strip()

if number_of_ports==2:
	proc = subprocess.Popen(["ifconfig eth7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	out=out.split("\n")
	for line in out:
		if "HWaddr" not in line:
			continue
		server_mac_2=line.strip().split()[-1]

#print "Switch Mac",switch_mac,"Server MAC",server_mac,"Source IP",source_ip
#if number_of_ports==2:
#	print "Switch Mac",switch_mac_2,"Server MAC",server_mac_2


child = pexpect.spawn('sudo /opt/netronome/srcpkg/dpdk-ns/tools/dpdk-setup.sh')
child.expect('Option:*')
child.sendline('20')
child.expect('Number of pages for node0:*')
child.sendline('2048')
child.expect('Number of pages for node1:*')
child.sendline('2048')
child.expect('Press enter to continue ...*')
child.sendline('')
child.expect('Option:*')
child.sendline('33')
os.chdir("/opt/pktgen-3.4.5")
#child = pexpect.spawn('sudo app/app/x86_64-native-linuxapp-gcc/pktgen -c 0x1f -n 1 -w 08:08.1 -- -m [1:2].0',cwd="/opt/pktgen-3.4.5")
child = pexpect.spawn('sudo app/app/x86_64-native-linuxapp-gcc/pktgen -c 0xffff -n 3 -w 08:08.1 -w 08:08.2 -- -p 0xf0 -P -m "[1:3].0, [4:6].1"')
child.sendline()

if type=="proxy" or type=="ddos_with_sig":
	child.sendline('set 0 src ip '+source_ip)
	child.sendline('set 0 dst ip '+attack_ip)
	child.sendline('set 0 src mac '+server_mac)
	child.sendline('set 0 dst mac '+switch_mac)
	child.sendline('set 0 size 1500')	
	child.sendline('set 0 rate '+str(attack_rate))
	child.sendline('set 0 proto udp')

	child.sendline('set 1 src ip '+source_ip)
	child.sendline('set 1 dst ip '+legit_address)
	child.sendline('set 1 src mac '+server_mac)
	child.sendline('set 1 dst mac '+switch_mac)
	child.sendline('set 1 size 1500')
	child.sendline('set 1 rate '+str(legit_traffic_rate))
	child.sendline('set 1 proto udp')

	if legit_traffic==1:
		child.sendline('start 1')
		print "SLEEEPING *******"
	time.sleep(legit_duration)
	print "Starting attack"	
	child.sendline('start 0')
	time.sleep(attack_duration)
	child.sendline('stop 0')
	time.sleep(10)
	child.sendline('stop 1')
	child.sendline('quit')



if type=="amon_proxy":
	#range 0 src ip 52.0.0.1 52.0.0.1 52.0.0.3 0.0.0.1

	#child.sendline('range 1 src ip '+legit_traffic_start+' '+source_ip+' '+legit_traffic_end+' 0.0.0.1')
	child.sendline('range 0 src ip '+source_ip+' '+source_ip+' '+source_ip+' 0.0.0.0')
	print 'range 0 src ip '+source_ip+' '+source_ip+' '+source_ip+' 0.0.0.0'

	#range 0 dst ip 57.0.0.1 57.0.0.1 57.0.0.1 0.0.0.0
	child.sendline('range 0 dst ip '+attack_ip+" "+attack_ip+" "+attack_ip+" 0.0.0.0")
	print 'range 0 dst ip '+attack_ip+" "+attack_ip+" "+attack_ip+" 0.0.0.0"
	#range 0 src mac fa:07:ad:ad:84:fc fa:07:ad:ad:84:fc fa:07:ad:ad:84:fc 00:00:00:00:00:00
	child.sendline('range 0 src mac '+server_mac+" "+server_mac+" "+server_mac+" 00:00:00:00:00:00")
	print 'range 0 src mac '+server_mac+" "+server_mac+" "+server_mac+" 00:00:00:00:00:00"
	#range 0 dst mac 7c:fe:90:f3:a1:41 7c:fe:90:f3:a1:41 7c:fe:90:f3:a1:41 00:00:00:00:00:00
	child.sendline('range 0 dst mac '+switch_mac+" "+switch_mac+" "+switch_mac+" 00:00:00:00:00:00")
	print 'range 0 dst mac '+switch_mac+" "+switch_mac+" "+switch_mac+" 00:00:00:00:00:00"
	#range 0 size  1500 1500 1500 0

	child.sendline('range 0 size 1500 1500 1500 0')	
	print 'range 0 size 1500 1500 1500 0'
	child.sendline('range 0 src port 1 1 256 1')
	print 'range 0 src port 1 1 256 1'
	child.sendline('range 0 dst port 15713 15713 15713 0')
	print 'range 0 dst port 15713 15713 15713 0'
	child.sendline('set 0 rate '+str(attack_rate))
	print 'set 0 rate '+str(attack_rate)
	#child.sendline('set 0 rate '+str(attack_rate))
	child.sendline('range 0 proto udp')
	print 'range 0 proto udp'
	child.sendline('enable 0 range')
	print 'enable 0 range'
	print "Starting attack"
	child.sendline('start 0')
	time.sleep(attack_duration)
	#time.sleep(1000)
	child.sendline('stop 0')
	#if legit_sources>=1:
	#	child.sendline('stop 1')
	child.sendline('quit')



if type=="ddos_without_sig":
	#range 0 src ip 52.0.0.1 52.0.0.1 52.0.0.3 0.0.0.1
	print "Legit: ",legit_traffic_start,legit_traffic_end
	print "Attack: ",source_ip_start,source_ip_end,

	#child.sendline('range 1 src ip '+legit_traffic_start+' '+legit_traffic_start+' '+legit_traffic_end+' 0.0.0.1')
	child.sendline('range 1 src ip '+legit_traffic_start+' '+legit_traffic_start+' '+legit_traffic_start+' 0.0.0.0')

	#child.sendline('range 0 src ip '+source_ip_start+' '+source_ip_start+' '+source_ip_end+' 0.0.0.1')
	child.sendline('range 0 src ip '+source_ip_start+' '+source_ip_start+' '+source_ip_start+' 0.0.0.0')

	#range 0 dst ip 57.0.0.1 57.0.0.1 57.0.0.1 0.0.0.0
	child.sendline('range 0,1 dst ip '+attack_ip+" "+attack_ip+" "+attack_ip+" 0.0.0.0")
	#range 0 src mac fa:07:ad:ad:84:fc fa:07:ad:ad:84:fc fa:07:ad:ad:84:fc 00:00:00:00:00:00
	child.sendline('range 0,1 src mac '+server_mac+" "+server_mac+" "+server_mac+" 00:00:00:00:00:00")
	#range 0 dst mac 7c:fe:90:f3:a1:41 7c:fe:90:f3:a1:41 7c:fe:90:f3:a1:41 00:00:00:00:00:00
	child.sendline('range 0,1 dst mac '+switch_mac+" "+switch_mac+" "+switch_mac+" 00:00:00:00:00:00")
	#range 0 size  1500 1500 1500 0

	child.sendline('range 0,1 size 1500 1500 1500 0')	
	child.sendline('range 0 src port 1 256 1 1')
	child.sendline('range 0 dst port 15713 15713 15713 0')
	child.sendline('range 1 src port 1 256 1 1')
	child.sendline('range 1 dst port 15713 15713 15713 0')
	print "Legit traffic rate",legit_traffic_rate,"Attack rate",attack_rate
	child.sendline('set 0 rate '+str(attack_rate))
	child.sendline('set 1 rate '+str(legit_traffic_rate))
	#child.sendline('set 0 rate '+str(attack_rate))
	child.sendline('range 0,1 proto udp')
	child.sendline('enable 0,1 range')


	#if legit_sources>=1:
	#	child.sendline('start 1')
	#	print "SLEEEPING *******",legit_duration
	#	time.sleep(legit_duration)

	print "Starting attack"
	child.sendline('start 0')
	time.sleep(attack_duration)
	#time.sleep(1000)
	child.sendline('stop 0')
	#if legit_sources>=1:
	#	child.sendline('stop 1')
	child.sendline('quit')



