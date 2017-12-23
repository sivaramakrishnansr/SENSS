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

proc = subprocess.Popen(["ifconfig eth6"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
out=out.split("\n")
for line in out:
	if "HWaddr" in line:
		server_mac_1=line.strip().split()[-1]
	if "inet addr" in line:
		source_ip=line.strip().split("inet addr:")[-1].split()[0].strip()
if number_of_ports==2:
	proc = subprocess.Popen(["ifconfig eth7"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	out=out.split("\n")
	for line in out:
		if "HWaddr" not in line:
			continue
		server_mac_2=line.strip().split()[-1]

print "Switch Mac",switch_mac_1,"Server MAC",server_mac_1,"Source IP",source_ip
if number_of_ports==2:
	print "Switch Mac",switch_mac_2,"Server MAC",server_mac_2


child = pexpect.spawn('sudo /opt/netronome/srcpkg/dpdk-ns/tools/dpdk-setup.sh')
child.expect('Option:*')
child.sendline('20')
child.expect('Number of pages for node0:*')
child.sendline('1024')
child.expect('Number of pages for node1:*')
child.sendline('1024')
child.expect('Press enter to continue ...*')
child.sendline('')
child.expect('Option:*')
child.sendline('33')
os.chdir("/opt/pktgen-3.4.5")
child = pexpect.spawn('sudo /opt/pktgen-3.4.5/app/app/x86_64-native-linuxapp-gcc/pktgen -c 0x1f -n 1 -w 08:08.1 -- -m [1:2].0')
child.expect('Pktgen:/>*')
child.sendline()
child.sendline('set 0 src ip '+source_ip)
child.sendline('set 0 dst ip '+attack_ip)
child.sendline('set 0 src mac '+server_mac_1)
child.sendline('set 0 dst mac '+switch_mac_1)
child.sendline('set 0 size 1500')
child.sendline('set 0 rate '+str(attack_rate))
child.sendline('start 0')
time.sleep(attack_duration)
child.sendline('stop 0')
time.sleep(3)
child.sendline('quit')

