
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
                                switch=ip[1]+"-"+ip[2]
                        else:
                                switch=ip[2]+"-"+ip[1]
                        switches.add(switch)
switches=list(switches)


list_of_cities=sorted(list(list_of_cities))


for city in list_of_cities:

	print "Removing up Quagga for ",city," .."
	try:
		url="i"+str(list_of_cities.index(city)+1)+".airtelsenss.senss"
		command_to_execute="sudo python /proj/SENSS/DHS/Setup/Clean/clean_router.py"
		print "Cleaning Router",url,command_to_execute
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		ssh.connect(url,username="satyaman", password="usc558l", timeout=360)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)	
		print ssh_stdout.readlines()

	except:
		print "Already Removed"
for switch in switches:
	try:
		url="i"+str(switch)+".airtelsenss.senss"
		command_to_execute="sudo python /proj/SENSS/DHS/Setup/Clean/clean_switch.py"
		print "Cleaning Switch",url,command_to_execute
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		ssh.connect(url,username="satyaman", password="usc558l",timeout=360)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)	
		print ssh_stdout.readlines()
	except:
		print "Already Removed"
	print
	print
