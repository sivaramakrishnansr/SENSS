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

import sys
import json
import paramiko
import getpass
import socket
import urllib2
import subprocess

type=sys.argv[1]
def start_attack():
        nodes={}
        two_ports=[]
	if type=="proxy":
	        f=open("nodes_proxy","r")
	if type=="ddos_with_sig":
	        f=open("nodes_ddos_with_sig","r")
	if type=="ddos_without_sig":
		f=open("nodes_ddos_without_sig","r")
	if type=="amon":
		f=open("nodes_amon","r")
	if type=="amon_proxy":
		f=open("nodes_amon_proxy","r")

        for line in f:
		if len(line.strip())==0:
			continue
                if "#" in line:
                        continue
			
		if type=="proxy" or type=="ddos_with_sig":
	                node=line.strip().split(" ")[0]
        	        number_of_ports=int(line.strip().split(" ")[1])
                	node_type=line.strip().split(" ")[2]
                	asn=line.strip().split(" ")[3]
	                server_url=line.strip().split(" ")[4]
        	        links_to=line.strip().split(" ")[5]
                	self=int(line.strip().split(" ")[6])
			attack_rate=line.strip().split(" ")[7]
			attack_duration=int(line.strip().split(" ")[8])
			server_mac=line.strip().split(" ")[9]
			switch_mac=line.strip().split(" ")[10]
			server_ip=line.strip().split(" ")[11]
			legit_traffic=line.strip().split(" ")[12]
			legit_traffic_rate=line.strip().split(" ")[13]
			legit_traffic_duration=line.strip().split(" ")[14]
			legit_address=line.strip().split(" ")[15]
			if node_type=="client":
				attack_ip=node.replace("hpc0","")+".0.0.1"
				continue
			if node_type=="proxy":
				continue
	                nodes[node]={}
        	        nodes[node]["node_type"]=node_type
                	nodes[node]["asn"]=asn
	                nodes[node]["server_url"]=server_url
        	        nodes[node]["links_to"]=links_to
                	nodes[node]["self"]=self
			nodes[node]["attack_rate"]=attack_rate
			nodes[node]["attack_duration"]=attack_duration
			nodes[node]["server_mac"]=server_mac
			nodes[node]["switch_mac"]=switch_mac
			nodes[node]["server_ip"]=server_ip
			nodes[node]["legit_traffic"]=legit_traffic
			nodes[node]["legit_traffic_rate"]=legit_traffic_rate
			nodes[node]["legit_traffic_duration"]=legit_traffic_duration
			nodes[node]["legit_address"]=legit_address

		if type=="ddos_without_sig":
	                node=line.strip().split(" ")[0]
			if node!="hpc057" and node!="hpc050":
				continue
        	        number_of_ports=int(line.strip().split(" ")[1])
                	node_type=line.strip().split(" ")[2]
                	asn=line.strip().split(" ")[3]
	                server_url=line.strip().split(" ")[4]
        	        links_to=line.strip().split(" ")[5]
                	self=int(line.strip().split(" ")[6])
			attack_rate=line.strip().split(" ")[7]
			attack_duration=int(line.strip().split(" ")[8])
			server_mac=line.strip().split(" ")[9]
			switch_mac=line.strip().split(" ")[10]
			legit_sources=line.strip().split(" ")[11]
			attack_sources=line.strip().split(" ")[12]
			legit_traffic_rate=line.strip().split(" ")[13]
			legit_traffic_duration=line.strip().split(" ")[14]
			if node_type=="client":
				attack_ip=node.replace("hpc0","")+".0.0.1"
				continue
	                nodes[node]={}
        	        nodes[node]["node_type"]=node_type
                	nodes[node]["asn"]=asn
	                nodes[node]["server_url"]=server_url
        	        nodes[node]["links_to"]=links_to
                	nodes[node]["self"]=self
			nodes[node]["attack_rate"]=attack_rate
			nodes[node]["attack_duration"]=attack_duration
			nodes[node]["server_mac"]=server_mac
			nodes[node]["switch_mac"]=switch_mac
			nodes[node]["legit_sources"]=legit_sources
			nodes[node]["attack_sources"]=attack_sources
			nodes[node]["legit_traffic_rate"]=legit_traffic_rate
			nodes[node]["legit_traffic_duration"]=legit_traffic_duration


        f.close()
	#user=raw_input("Username: ").strip()
	user="satyaman"
	#password=getpass.getpass()
	password="&5h$19tZrunu"
	for node in nodes:
                print "Node: ",node," "
	        ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	ssh.connect(node,username=user, password=password, timeout=3)
		if type=="proxy" or type=="ddos_with_sig":
			print "sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+nodes[node]["server_mac"]+" "+nodes[node]["server_ip"]+" "+nodes[node]["legit_traffic"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"]+" "+nodes[node]["legit_address"]
			stdin,stdout,stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+nodes[node]["server_mac"]+" "+nodes[node]["server_ip"]+" "+nodes[node]["legit_traffic"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"]+" "+nodes[node]["legit_address"]) 
			print "Attack IP: ",attack_ip
			print "Attack Duration: ",nodes[node]["attack_duration"]
			print "Attack Rate: ",nodes[node]["attack_rate"]
			print
		if type=="ddos_without_sig":
			print "sudo /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+nodes[node]["asn"]+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+ nodes[node]["server_mac"]+" "+nodes[node]["legit_sources"]+" "+nodes[node]["attack_sources"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"]
			stdin,stdout,stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+nodes[node]["asn"]+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+ nodes[node]["server_mac"]+" "+nodes[node]["legit_sources"]+" "+nodes[node]["attack_sources"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"])
			print "Attack IP: ",attack_ip
			print "Source IP: ",node
			print "Attack Duration: ",nodes[node]["attack_duration"]
			print "Attack Rate: ",nodes[node]["attack_rate"]

			print

if __name__ == '__main__':
	start_attack()
