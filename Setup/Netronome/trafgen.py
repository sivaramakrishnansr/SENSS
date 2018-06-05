#!/usr/bin/env python
import time
import os
import pexpect
import subprocess
import sys

#Command line arguments
number_of_ports=1
attack_ip=sys.argv[1]
attack_duration=int(sys.argv[2])
attack_rate=sys.argv[3]
switch_mac=sys.argv[4]
server_mac=sys.argv[5]
source_ip=sys.argv[6]
legit_traffic=int(sys.argv[7])
legit_traffic_rate=sys.argv[8]

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

print "Switch Mac",switch_mac,"Server MAC",server_mac,"Source IP",source_ip
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
child.sendline('set 0 src ip '+source_ip)
child.sendline('set 0 dst ip '+attack_ip)
child.sendline('set 0 src mac '+server_mac)
child.sendline('set 0 dst mac '+switch_mac)
child.sendline('set 0 size 1500')
child.sendline('set 0 rate '+str(attack_rate))
child.sendline('set 0 proto udp')

child.sendline('set 1 src ip '+source_ip)
child.sendline('set 1 dst ip 57.0.0.5')
child.sendline('set 1 src mac '+server_mac)
child.sendline('set 1 dst mac '+switch_mac)
child.sendline('set 1 size 1500')
child.sendline('set 1 rate '+str(legit_traffic_rate))
child.sendline('set 1 proto udp')

if legit_traffic==1:
	child.sendline('start 1')
print "SLEEEPING *******"
time.sleep(30)
	
child.sendline('start 0')
#time.sleep(attack_duration)
time.sleep(60)
child.sendline('stop 0')
time.sleep(10)
child.sendline('stop 1')
child.sendline('quit')

