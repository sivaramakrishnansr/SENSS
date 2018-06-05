#
# Copyright (C) 2016 University of Southern California.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import sys
import json
import paramiko
import getpass
import socket
import urllib2
import subprocess

def configure_attack_nodes():
	nodes=[]
	two_ports=[]
	f=open("attack_nodes","r")
	for line in f:
		if "#" in line:
			continue
		node=line.strip().split(" ")[0]
		nodes.append(node)
	f.close()

	password=getpass.getpass()
	for node in nodes:
		print "Node: ",node," "
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(node,username="satyaman", password=password, timeout=3)
		#Patching netronome
		stdin, stdout, stderr = ssh.exec_command("sudo sed 's/link.link_speed = ETH_SPEED_NUM_NONE/link.link_speed = ETH_SPEED_NUM_40G/g' -i /opt/netronome/srcpkg/dpdk-ns/drivers/net/nfp/nfp_net.c")
		data=stdout.readlines()

		stdin, stdout, stderr = ssh.exec_command("sudo apt-get install python-pexpect")
		data=stdout.readlines()

		#Make DPDK
		print "Making DPDK"
		stdin, stdout, stderr = ssh.exec_command("cd /opt/netronome/srcpkg/dpdk-ns/ ; sudo make")
		data=stdout.readlines()
		print data

		#Copying pktgen
		stdin, stdout, stderr = ssh.exec_command("sudo cp /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5.zip /opt/")
		data=stdout.readlines()

		#removing
		#print "Removing pktgen"
		stdin, stdout, stderr = ssh.exec_command("cd /opt/; sudo rm -rf /opt/pktgen-3.4.5")
		data=stdout.readlines()

		#extracting pktgen
		print "Extracting pktgen"		
		stdin, stdout, stderr = ssh.exec_command("cd /opt/; sudo unzip /opt/pktgen-3.4.5.zip")
		data=stdout.readlines()

		#Cleaning
		#print "Cleaning pktgen"		
		stdin, stdout, stderr = ssh.exec_command("; cd /opt/pktgen-3.4.5;sudo make clean RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc")
		data=stdout.readlines()
	
		#Copying lua
		print "Copying lua"
		stdin, stdout, stderr = ssh.exec_command("sudo cp /proj/SENSS/lua-5.3.4.tar.gz /opt/pktgen-3.4.5/lib/lua/")
		data=stdout.readlines()

		#Making lua with patch
		#print "Making only lua"
		stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5/lib/lua ; sudo make RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc")
		data=stdout.readlines()
		#print data

		#creating directories
		#print "Creating recursive directories"
		stdin, stdout, stderr = ssh.exec_command("sudo mkdir -p /opt/pktgen-3.4.5/lib/lua/src/lib/lua/src/x86_64-native-linuxapp-gcc/lib/")
		data=stdout.readlines()

		#Copying files
		stdin, stdout, stderr = ssh.exec_command("sudo cp /opt/pktgen-3.4.5/lib/lua/lua-5.3.4/src/src/x86_64-native-linuxapp-gcc/lib/librte_lua.a /opt/pktgen-3.4.5/lib/lua/src/lib/lua/src/x86_64-native-linuxapp-gcc/lib/")
		data=stdout.readlines()

		#Making pktgen
		print "Making pktgen"
		stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5;sudo make RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc")
		data=stdout.readlines()
		#print data
		print
if __name__ == '__main__':
	configure_attack_nodes()



