
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
import json
import sys
import os
import paramiko

ip_dict={}
file_to_read=open("/proj/SENSS/DHS/Setup/quagga_input","r")
for line in file_to_read:
	line=line.strip().split("qwerty123")
	ip=line[0]
	value=json.loads(line[1])
	ip_dict[ip]=value

list_of_cities=set()
switches=set()
for key,value in ip_dict.iteritems():
	list_of_cities.add(key)
	for ips in value:
		for ip,asn in ips.iteritems():
			ip=ip.split(".")
			if int(ip[1])<int(ip[2]):
				switch=ip[1]+"a"+ip[2]
			else:
				switch=ip[2]+"a"+ip[1]
			switches.add(switch)
switches=list(switches)
print switches

list_of_cities=list(list_of_cities)
controller_ip=sys.argv[1]
list_of_cities=sorted(list_of_cities)
print list_of_cities

for city in list_of_cities:
	print "Setting up Quagga for ",city," .."
	try:
		url="i"+str(list_of_cities.index(city)+1)+".dhs.senss"
		command_to_execute="sudo python /proj/SENSS/DHS/Setup/quagga_setup.py "+city
		print url,command_to_execute
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		ssh.connect(url,username="satyaman", password="usc558l", timeout=360)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)	
		print ssh_stdout.readlines()
	except:
		print "Already Added"
for switch in switches:
	#Script for the switch
	try:
		url="i"+str(switch)+".dhs.senss"
		command_to_execute="sudo python /proj/SENSS/DHS/Setup/switch_setup.py "+controller_ip+" "+switch
		print url,command_to_execute
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		ssh.connect(url,username="satyaman", password="usc558l",timeout=360)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)	
		print ssh_stdout.readlines()
	except:
		print "Already Added"
	print
	print
