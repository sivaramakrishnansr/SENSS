#
# Copyright (C) 2018 University of Southern California.
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

import os
import sys
import subprocess
import json


ip_dict={}
file_to_read=open("quagga_input","r")
for line in file_to_read:
 	line=line.strip().split("qwerty123")
        ip=line[0]
        value=json.loads(line[1])
        ip_dict[ip]=value

list_of_cities=set()
for key,value in ip_dict.iteritems():
	print key,value
	list_of_cities.add(key)

list_of_cities=sorted(list(list_of_cities))
print list_of_cities

city=sys.argv[1]


cmd_to_execute="sudo apt-get install python-netifaces"
proc = subprocess.Popen(cmd_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
proc.wait()

os.system("sudo apt-get update && sudo apt-get install --assume-yes quagga")

print "Generating Files" 
#Generates the BGPD file
city_number=str(list_of_cities.index(city)+1)
file_to_write=open("/etc/quagga/bgpd.conf","w")
file_to_write.write("hostname i"+city_number+"in\n")
file_to_write.write("password en\n")
file_to_write.write("enable password en\n")
file_to_write.write("router bgp "+city_number+"\n")
file_to_write.write(" network "+city_number+".0.0.0/8\n")
for item in ip_dict[city]:
	for neighbor_ip,neighbor_value in item.iteritems():
		file_to_write.write(" neighbor "+neighbor_ip+" remote-as "+neighbor_value+"\n")
file_to_write.close()

#Generates the Debian Config file to be Telnet"d from different locations
file_to_write=open("/etc/quagga/debian.conf","w")
file_to_write.write('vtysh_enable=yes\n')
file_to_write.write('zebra_options="  --daemon -A 127.0.0.1"\n')
file_to_write.write('bgpd_options="   --daemon "\n')
file_to_write.write('ospfd_options="  --daemon -A 127.0.0.1"\n')
file_to_write.write('ospf6d_options=" --daemon -A ::1"\n')	
file_to_write.write('ripd_options="   --daemon -A 127.0.0.1"\n')
file_to_write.write('ripngd_options=" --daemon -A ::1"\n')
file_to_write.write('isisd_options="  --daemon -A 127.0.0.1"\n')
file_to_write.write('babeld_options=" --daemon -A 127.0.0.1"\n')
file_to_write.write('watchquagga_enable=yes\n')
file_to_write.write('watchquagga_options=(--daemon)\n')
file_to_write.close()

#Generates the Daemon file for Quagga
file_to_write=open("/etc/quagga/daemons","w")
file_to_write.write("zebra=yes\n")
file_to_write.write("bgpd=yes\n")
file_to_write.write("ospfd=no\n")
file_to_write.write("ospf6d=no\n")
file_to_write.write("ripd=no\n")
file_to_write.write("ripngd=no\n")
file_to_write.write("isisd=no\n")
file_to_write.close()

#Generates the Zebra file for Quagga
#cmd_to_execute='sudo dpkg -i /proj/SENSS/python-netifaces_0.6-2ubuntu1_amd64.deb'
#cmd_to_execute='sudo dpkg -i /proj/SENSS/python-netifaces_0.8-3build1_i386.deb'
import netifaces
interface_list = netifaces.interfaces()
interface_dict={}
for interface in interface_list:
        try:
                address=netifaces.ifaddresses(interface)
                interface_dict[interface]=address[netifaces.AF_INET][0]['addr']
        except:
                a=1
file_to_write=open('/etc/quagga/zebra.conf','w')
file_to_write.write('hostname zebra\n')
file_to_write.write('password en\n')
file_to_write.write('enable password en\n')
for key,value in interface_dict.iteritems():
        file_to_write.write('interface '+str(key)+"\n")
        file_to_write.write('   ip address '+str(value)+'/24\n')
file_to_write.close()
os.system("sudo service quagga restart")

print "Done ",item

	
