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
import time
import os

def init_database(ssh,nodes,is_client):
	stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/init.py usc558l")
	data=stdout.readlines()
	if is_client==1:
		return
	for node,node_data in nodes.iteritems():
		stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/insert_topo.py "+node+" "+node_data["links_to"]+" "+str(node_data["self"]))
		data=stdout.readlines()

def add_client_entries(ssh,as_name,server_url,links_to,self):
	if links_to=="None":
		return
	stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/insert_senss_client.py usc558l "+as_name+" "+server_url+" "+links_to+" "+self)
	data=stdout.readlines()


def start_ryu(ssh):
	stdin, stdout, stderr = ssh.exec_command("killall screen")
	data=stdout.readlines()
	stdin, stdout, stderr = ssh.exec_command("screen -d -m ryu-manager /proj/SENSS/SENSS_git/SENSS/ryu/ryu-master/ryu/app/ofctl_rest.py")
	data=stdout.readlines()
	print "Started RYU controller"

def start_monitor_flows(ssh,multiply,legit_address):
	stdin, stdout, stderr = ssh.exec_command("screen -d -m sudo python /var/www/html/SENSS/UI_client_server/Server/monitor_flows.py "+str(multiply)+" "+str(legit_address))
	data=stdout.readlines()
	print "Started Monitoring flows controller"


def return_ips(node):
	first_octet=node.replace("hpc0","")
	ip_1=first_octet+".0.0.1"
	ip_2=first_octet+".1.0.1"
	return ip_1,ip_2,first_octet

def get_interface(ssh,vnf):
	stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py --status")
	for item in stdout.readlines():
		if vnf in item.strip() and "if=eth" in item.strip():
			interface=item.strip().split(" ")[3].split("=")[-1]
	return interface

def get_dpid(controller_ip):
        method = "GET"
       	handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/switches")
        request.get_method = lambda: method
	dpid=0
	while True:
        	connection = opener.open(request)
        	data = json.loads(connection.read())
		print data
		for item in data:
			dpid=item
		print dpid
		if dpid!=0:
			break
		time.sleep(3)
	return dpid

def add_forwarding_rules(controller_ip,dpid,in_port,out_port):
        data_to_send={'dpid': int(dpid),'priority':1,'match':{'in_port':in_port},'actions':[{'type':'OUTPUT','port':out_port}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()

def add_forwarding_rules_server(controller_ip,dpid,in_port,out_port):
        data_to_send={'dpid': int(dpid),'priority':33333,'match':{'in_port':in_port,'tcp_src':80,'ip_proto': 6, 'eth_type': 2048},'actions':[{'type':'OUTPUT','port':out_port}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()

def add_forwarding_rules_2(controller_ip,dpid,in_port,out_port_1,out_port_2):
        data_to_send={'dpid': int(dpid),'priority':1,'match':{'in_port':in_port},'actions':[{'type':'OUTPUT','port':out_port_1},{'type':'OUTPUT','port':out_port_2}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()

def print_data(data):
	for item in data:
		print item.strip()


def configure_nodes():
	nodes={}
	attack_type=sys.argv[1]
	two_ports=[]
	if attack_type=="proxy":
		f=open("nodes_proxy","r")
	if attack_type=="ddos_with_sig":
		f=open("nodes_ddos_with_sig","r")
	if attack_type=="ddos_without_sig":
		f=open("nodes_ddos_without_sig","r")
	if attack_type=="amon":
		f=open("nodes_amon","r")
	if attack_type=="amon_proxy":
		f=open("nodes_amon_proxy","r")
	#Deter node name/Number of netronome ports connected/node type/AS name/server url/links to/self
	for line in f:
		if "#" in line:
			continue
		node=line.strip().split(" ")[0]
		number_of_ports=int(line.strip().split(" ")[1])
		node_type=line.strip().split(" ")[2]
		asn=line.strip().split(" ")[3]
		server_url=line.strip().split(" ")[4]
		legit_address=line.strip().split(" ")[-1]
		if node_type=="proxy":
			proxy_ip=line.strip().split(" ")[11]
		links_to=str(line.strip().split(" ")[5])
		self=int(line.strip().split(" ")[6])
		if attack_type=="ddos_without_sig":
			legit_nodes=int(line.strip().split(" ")[11])
			attack_nodes=int(line.strip().split(" ")[12])
			total_nodes=legit_nodes+attack_nodes
		nodes[node]={}
		nodes[node]["node_type"]=node_type
		nodes[node]["asn"]=asn
		nodes[node]["server_url"]=server_url
		nodes[node]["links_to"]=links_to
		nodes[node]["self"]=self
		nodes[node]["legit_address"]=legit_address
		if attack_type=="ddos_without_sig":
			nodes[node]["total_nodes"]=total_nodes
		if number_of_ports==2:
			two_ports.append(node)
		if attack_type=="ddos_without_sig":
			nodes[node]["legit_address"]=1
	f.close()

	#user=raw_input("Usename: ").strip()
	user="satyaman"
	#password=getpass.getpass()
	password="&5h$19tZrunu"
	install={}

	f=open("install","r")
	for line in f:
		type=line.strip().split(",")[0]
		flag=line.strip().split(",")[1]
		install[type]=flag
	f.close()

	for node in nodes:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(node,username=user, password=password, timeout=3)
		ip_1,ip_2,first_octet=return_ips(node)
		controller_ip=socket.gethostbyname(node)
		print "Node: ",node

		#Start RYU
		start_ryu(ssh)
		print "Started RYU"
		
		#Init database
		if nodes[node]["node_type"]=="client":
			init_database(ssh,nodes,1)
		else:
			init_database(ssh,nodes,0)
		print "Initialised DB"

		if nodes[node]["node_type"]=="client":
			for node_1,values in nodes.iteritems():
				self="0"
				if values["node_type"]=="client":
					self="1"
				#print "Addding",values["asn"],values["server_url"],values["links_to"],self
				add_client_entries(ssh,values["asn"],values["server_url"],values["links_to"],self)
			print "Added client entries"

		if nodes[node]["node_type"]=="server":
			if node in two_ports:
				start_monitor_flows(ssh,2,nodes[node]["legit_address"])
			else:
				start_monitor_flows(ssh,1,nodes[node]["legit_address"])
		

		#Restart apache
		stdin, stdout, stderr = ssh.exec_command("sudo service apache2 restart")
		data=stdout.readlines()

		#OVS SETUP
		if node in two_ports:
			stdin, stdout, stderr = ssh.exec_command("sudo sh /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/ovs_two_ports.sh")
			data=stdout.readlines()
			#Add controller 
			stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl set-controller br0 tcp:"+controller_ip+":6633")
			data=stdout.readlines()
			dpid=get_dpid(controller_ip)
			add_forwarding_rules(controller_ip,dpid,1,3)		
			add_forwarding_rules(controller_ip,dpid,3,1)		
			add_forwarding_rules(controller_ip,dpid,5,1)		
			add_forwarding_rules_2(controller_ip,dpid,4,1,2)		
		if node not in two_ports:
			stdin, stdout, stderr = ssh.exec_command("sudo sh /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/ovs_one_port.sh")
			data=stdout.readlines()
			#Add controller 
			stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl set-controller br0 tcp:"+controller_ip+":6633")
			data=stdout.readlines()
			dpid=get_dpid(controller_ip)
			add_forwarding_rules(controller_ip,dpid,1,2)		
			add_forwarding_rules(controller_ip,dpid,2,1)
			add_forwarding_rules_server(controller_ip,dpid,2,1)		
			add_forwarding_rules_server(controller_ip,dpid,1,2)		
			add_forwarding_rules(controller_ip,dpid,3,1)		
			add_forwarding_rules(controller_ip,dpid,4,1)		
		print ("\n")
				

if __name__ == '__main__':
	configure_nodes()




