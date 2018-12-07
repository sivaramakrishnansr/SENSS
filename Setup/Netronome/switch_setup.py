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

import serial
import sys
import pexpect
from time import sleep
from serial import SerialException
import time

port_mapping={}
f=open("port_mapping","r")
for line in f:
	if "#" in line:
		continue
	interface=line.strip().split(" ")[0]
	vlan=line.strip().split(" ")[1]
	switch_ip=line.strip().split(" ")[2]
	server_ip=line.strip().split(" ")[3]
	asn=line.strip().split(" ")[4]
	port_mapping[interface]={}
	port_mapping[interface]["vlan"]=vlan
	port_mapping[interface]["switch_ip"]=switch_ip
	port_mapping[interface]["server_ip"]=server_ip
	port_mapping[interface]["asn"]=asn
f.close()

ser = serial.Serial()
ser.baudrate = 115200
ser.port="/dev/ttyUSB0"
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.open()

ser.write(unicode("enable\n"))
try:
	output=ser.readline()
except:
	a=1

ser.write(unicode("configure terminal\n"))
try:
	output=ser.readline()
except:
	a=1

#Lets set the speed for all ports
for i in range(1,32):
	#continue
	#if i!=3:
	#	continue
	interface="1/"+str(i)
	output_string="interface ethernet "+interface+"\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1
	time.sleep(0.75)

	output_string="shutdown\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1
	time.sleep(0.75)
	output_string="speed 40G\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1
	time.sleep(0.75)
	output_string="no shutdown\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1
	time.sleep(0.75)
	output_string="exit\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1
	time.sleep(0.75)

#Lets set the ip address on each interface
for interface,data in port_mapping.iteritems():
	#if interface!="1/1":
	#	continue
	print interface
	vlan=data["vlan"]
	switch_ip=data["switch_ip"]
	output_string="vlan "+vlan+"\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1

	time.sleep(0.75)
	output_string="exit\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1

	time.sleep(0.75)
	output_string="interface ethernet "+interface+" switchport access vlan "+vlan+"\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1

	time.sleep(0.75)
	output_string="interface vlan "+vlan+"\n"	
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1
	
	time.sleep(0.75)
	output_string="ip address "+switch_ip+" 255.255.255.0\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1

	time.sleep(0.75)
	output_string="exit\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1

#Let assign BGP
output_string="router bgp 1000\n"
ser.write(unicode(output_string))
try:
	output=ser.readline()
except:
	a=1
	time.sleep(0.75)

for interface,data in port_mapping.iteritems():
	#if interface!="1/1":
	#	continue
	print interface
	asn=data["asn"]
	server_ip=data["server_ip"]
	time.sleep(0.75)
	output_string="neighbor "+server_ip+" remote-as "+asn+"\n"
	ser.write(unicode(output_string))
	try:
		output=ser.readline()
	except:
		a=1

output_string="exit\n"	
ser.write(unicode(output_string))
try:
	output=ser.readline()
except:
	a=1
