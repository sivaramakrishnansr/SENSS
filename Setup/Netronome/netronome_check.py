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
import time

def init_database(ssh,nodes,is_client):
	print "HERE"
	stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/init.py usc558l")
	data=stdout.readlines()
	for i in data:	
		print data
	print "Initialised database"
	if is_client==1:
		return
	print "Adding AS_URLS"
	for node,node_data in nodes.iteritems():
		#if node=="hpc056":
		#	continue
		stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/insert_topo.py "+node+" "+node_data["links_to"]+" "+str(node_data["self"]))
		data=stdout.readlines()
		for i in data:
			print data	


def add_client_entries(ssh,as_name,server_url,links_to,self):
	stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/insert_senss_client.py usc558l "+as_name+" "+server_url+" "+links_to+" "+self)
	data=stdout.readlines()
	print data


def copy_files(ssh):
	stdin, stdout, stderr = ssh.exec_command("sudo cp -rf /proj/SENSS/SENSS_git/* /var/www/html/")
	data=stdout.readlines()
	print "Copied files"
	

def install_dependencies(ssh):
	stdin, stdout, stderr = ssh.exec_command("sudo service quagga stop")
	data=stdout.readlines()

	stdin, stdout, stderr = ssh.exec_command("/proj/SENSS/SENSS_git/SENSS/Setup/Netronome/install_dependencies.sh")
	data=stdout.readlines()
	print data
	stdin, stdout, stderr = ssh.exec_command("cd /users/satyaman/ryu/ryu-master; sudo python /users/satyaman/ryu/ryu-master/setup.py install")
	data=stdout.readlines()	
	print "Installed dependencies"

def start_ryu(ssh):
	stdin, stdout, stderr = ssh.exec_command("killall screen")
	data=stdout.readlines()
	stdin, stdout, stderr = ssh.exec_command("screen -d -m ryu-manager /proj/SENSS/SENSS_git/SENSS/ryu/ryu-master/ryu/app/ofctl_rest.py")
	data=stdout.readlines()
	print "Started RYU controller"

def start_monitor_flows(ssh,multiply,filter_1,filter_2):
	print filter_1,filter_2
	stdin, stdout, stderr = ssh.exec_command("screen -d -m sudo python /var/www/html/SENSS/UI_client_server/Server/monitor_flows.py "+str(multiply)+" "+filter_1+" "+filter_2)
	data=stdout.readlines()
	print "Started Monitoring flows controller"

def start_ovs(ssh):
	stdin, stdout, stderr = ssh.exec_command("sudo /opt/netronome/bin/ovs-ctl stop")
	data=stdout.readlines()
	stdin, stdout, stderr = ssh.exec_command("sudo /opt/netronome/bin/ovs-ctl start")
	data=stdout.readlines()
	print "Started OVS on Netronome"

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

def setup_ovs(ssh,port_1,port_2,port_request_1,port_request_2,interface,setup_bridge):
	if setup_bridge==False:
		stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl --if-exist del-br br0")
		data=stdout.readlines()

		stdin, stdout, stderr = ssh.exec_command('sudo ovs-vsctl add-br br0 -- set Bridge br0 "protocols=OpenFlow13"')
		data=stdout.readlines()

		stdin, stdout, stderr = ssh.exec_command("sudo ovs-ofctl -O OpenFlow13 del-flows br0")
		data=stdout.readlines()

		stdin, stdout, stderr = ssh.exec_command("sudo ovs-ofctl -O OpenFlow13 del-groups br0 group_id=0")
		data=stdout.readlines()

	stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl add-port br0 "+port_1+" -- set Interface "+port_1+" ofport_request="+str(port_request_1))
	data=stdout.readlines()

	stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl add-port br0 "+port_2+" -- set Interface "+port_2+" ofport_request="+str(port_request_2))
	data=stdout.readlines()

	stdin, stdout, stderr = ssh.exec_command("ifconfig "+port_2+" up")
	data=stdout.readlines()

	stdin, stdout, stderr = ssh.exec_command("ifconfig "+interface+" up")
	data=stdout.readlines()

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
	
def configure_pktgen_nodes(ssh):
	#Make DPDK

	#Patching netronome
        stdin, stdout, stderr = ssh.exec_command("sudo sed 's/link.link_speed = ETH_SPEED_NUM_NONE/link.link_speed = ETH_SPEED_NUM_40G/g' -i /opt/netronome/srcpkg/dpdk-ns/drivers/net/nfp/nfp_net.c")
        data=stdout.readlines()
	print "Patching netronome"
	print_data(data)

	#Make DPDK
	print "Making DPDK"
	stdin, stdout, stderr = ssh.exec_command("cd /opt/netronome/srcpkg/dpdk-ns/ ; sudo make")
	data=stdout.readlines()	
	print_data(data)



	#Copying pktgen
	print "Copying pktgen"
        stdin, stdout, stderr = ssh.exec_command("sudo cp /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5.zip /opt/")
        data=stdout.readlines()
	print_data(data)

        #removing
        print "Removing pktgen"
        stdin, stdout, stderr = ssh.exec_command("sudo rm -rf /opt/pktgen-3.4.5")
        data=stdout.readlines()
	print_data(data)


        #extracting pktgen
        print "Extracting pktgen"
        stdin, stdout, stderr = ssh.exec_command("cd /opt/; sudo unzip /opt/pktgen-3.4.5.zip")
        data=stdout.readlines()
	print_data(data)


        #Cleaning
        print "Cleaning pktgen"
        stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5;sudo make clean RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc",get_pty=True)
        #stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5;sudo make clean RTE_SDK=$RTE_SDK RTE_TARGET=$RTE_TARGET",get_pty=True)
        data=stdout.readlines()
	print_data(data)

        #Copying lua
        print "Copying lua"
        stdin, stdout, stderr = ssh.exec_command("sudo cp /proj/SENSS/lua-5.3.4.tar.gz /opt/pktgen-3.4.5/lib/lua/")
        data=stdout.readlines()
	print_data(data)

        #Making lua with patch
        print "Making only lua"
        stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5/lib/lua ; sudo make RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc",get_pty=True)
        #stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5/lib/lua ; sudo make RTE_SDK=$RTE_SDK RTE_TARGET=$RTE_TARGET",get_pty=True)
        data=stdout.readlines()
        #print data
	print_data(data)

        #creating directories
        print "Creating recursive directories"
        stdin, stdout, stderr = ssh.exec_command("sudo mkdir -p /opt/pktgen-3.4.5/lib/lua/src/lib/lua/src/x86_64-native-linuxapp-gcc/lib/")
        data=stdout.readlines()
	print_data(data)

        #Copying files
	print "copying files"
        stdin, stdout, stderr = ssh.exec_command("sudo cp /opt/pktgen-3.4.5/lib/lua/lua-5.3.4/src/src/x86_64-native-linuxapp-gcc/lib/librte_lua.a /opt/pktgen-3.4.5/lib/lua/src/lib/lua/src/x86_64-native-linuxapp-gcc/lib/")
        data=stdout.readlines()
	print_data(data)

        #Making pktgen
        print "Making pktgen"
        stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5;sudo make RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc; pwd",get_pty=True)
        #stdin, stdout, stderr = ssh.exec_command("cd /opt/pktgen-3.4.5;sudo make RTE_SDK=$RTE_SDK RTE_TARGET=$RTE_TARGET; pwd",get_pty=True)
        data=stdout.readlines()
	print_data(data)
        #print


def configure_nodes():
	nodes={}
	attack_type=sys.argv[1]
	two_ports=[]
	if attack_type=="proxy":
		f=open("nodes","r")
	if attack_type=="ddos":
		f=open("nodes_1","r")
		
	#Deter node name/Number of netronome ports connected/node type/AS name/server url/links to/self
	for line in f:
		if "#" in line:
			continue
		print line.strip()
		node=line.strip().split(" ")[0]
		number_of_ports=int(line.strip().split(" ")[1])
		node_type=line.strip().split(" ")[2]
		asn=line.strip().split(" ")[3]
		server_url=line.strip().split(" ")[4]
		links_to=line.strip().split(" ")[5]
		self=int(line.strip().split(" ")[6])
		nodes[node]={}
		nodes[node]["node_type"]=node_type
		nodes[node]["asn"]=asn
		nodes[node]["server_url"]=server_url
		nodes[node]["links_to"]=links_to
		nodes[node]["self"]=self
		if number_of_ports==2:
			two_ports.append(node)
	f.close()

	password=getpass.getpass()
	
	for node in nodes:
		#if node!="hpc042":
		#	continue
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(node,username="satyaman", password=password, timeout=3)
		ip_1,ip_2,first_octet=return_ips(node)
		controller_ip=socket.gethostbyname(node)
		print "Node: ",node," ",controller_ip,node in two_ports

		#Install dependencies
		#install_dependencies(ssh)

		#Start RYU
		start_ryu(ssh)
		print "Started RYU"
		
		#Init database
		if nodes[node]["node_type"]=="client":
			init_database(ssh,nodes,1)
		else:
			init_database(ssh,nodes,0)
		print "Initialised DB"
		#Resetting database to the address
		#enter client values
		if nodes[node]["node_type"]=="client":
			for node,values in nodes.iteritems():
				self="0"
				if values["node_type"]=="client":
					self="1"
				print "Addding",values["asn"],values["server_url"],values["links_to"],self
				add_client_entries(ssh,values["asn"],values["server_url"],values["links_to"],self)
			print "Added client entries"

		#Start monitoring flows
		#ip_1 is the source ip
		if nodes[node]["node_type"]=="server":
			if node in two_ports:
				start_monitor_flows(ssh,2,"ipv4,nw_src="+ip_1+",nw_dst=57.0.0.1","ipv4,nw_src="+ip_1+",nw_dst=57.0.0.5")
			else:
				start_monitor_flows(ssh,1,"ipv4,nw_src="+ip_1+",nw_dst=57.0.0.1","ipv4,nw_src="+ip_1+",nw_dst=57.0.0.5")


		#Start OVS on netronome NIC
		#start_ovs(ssh)

		#Add IP address to interface_1
		#stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py -b nfp_netvf 08:08.0")
		#data=stdout.readlines()
		#print data
		#interface_1=get_interface(ssh,"08:08.0")
		#dummy_ip="200.0.0.1"
		#stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_1+" "+dummy_ip)
		#data=stdout.readlines()
		#stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_1+" "+dummy_ip)
		#data=stdout.readlines()
		#stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_1+" "+ip_1)
		#data=stdout.readlines()


		#copy server/client files
		#copy_files(ssh)



		#Install dpdk pktgen
		#if nodes[node]["node_type"]=="server":
		#	print "Configuring pktgen"
		#	configure_pktgen_nodes(ssh)

		#Restart apache
		stdin, stdout, stderr = ssh.exec_command("sudo service apache2 restart")
		data=stdout.readlines()
		


		#OVS SETUP
		if node in two_ports:
			print "In two ports"
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
			add_forwarding_rules(controller_ip,dpid,3,1)		
			add_forwarding_rules(controller_ip,dpid,4,1)		
			

		#Overwrite the constants file
		dpid=get_dpid(controller_ip)
		string_to_write="<?php\n"
		string_to_write=string_to_write+'const CONTROLLER_BASE_URL = "http://'+node+':8080",\n'
	    	string_to_write=string_to_write+"SWITCH_DPID = "+str(dpid)+";\n"
		stdin, stdout, stderr = ssh.exec_command("sudo rm /var/www/html/SENSS/UI_client_server/Server/constants.php")
		data=stdout.readlines()
		stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /var/www/html/SENSS/UI_client_server/Server/constants.php")
		data=stdout.readlines()
		continue
		#Config zebra
		string_to_write="hostname zebra\n"
		string_to_write=string_to_write+"password en\n"
		string_to_write=string_to_write+"enable password en\n"
		string_to_write=string_to_write+"interface "+interface_1+"\n"
		string_to_write=string_to_write+" ip address "+ip_1+"/32\n"
		#if node in two_ports:
		#	string_to_write=string_to_write+"interface "+interface_2+"\n"
		#	string_to_write=string_to_write+" ip address "+ip_2+"/32"

		stdin, stdout, stderr = ssh.exec_command("sudo rm /etc/quagga/zebra.conf")
		data=stdout.readlines()
		stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /etc/quagga/zebra.conf")
		data=stdout.readlines()

		#Configure daemons
		string_to_write="zebra=yes\n"
		string_to_write=string_to_write+"bgpd=yes\n"
		string_to_write=string_to_write+"ospfd=no\n"
		string_to_write=string_to_write+"ospf6d=no\n"
		string_to_write=string_to_write+"ripd=no\n"
		string_to_write=string_to_write+"ripngd=no\n"
		string_to_write=string_to_write+"isisd=no\n"

		stdin, stdout, stderr = ssh.exec_command("sudo rm /etc/quagga/daemons")
		data=stdout.readlines()
		stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /etc/quagga/daemons")
		data=stdout.readlines()

		#Condigure bgpd
		string_to_write="hostname "+node+"\n"
		string_to_write=string_to_write+"password en\n"
		string_to_write=string_to_write+"enable password en\n"
		string_to_write=string_to_write+"router bgp "+first_octet+"\n"
		string_to_write=string_to_write+" network "+first_octet+".0.0.0/8\n"
		string_to_write=string_to_write+" neighbor "+first_octet+".0.0.2 remote-as 1000\n"
		#if node in two_ports:
		#	string_to_write=string_to_write+" neighbor "+first_octet+".1.0.2 remote-as 1000\n"
		stdin, stdout, stderr = ssh.exec_command("sudo rm /etc/quagga/bgpd.conf")
		data=stdout.readlines()

		stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /etc/quagga/bgpd.conf")
		data=stdout.readlines()
		stdin, stdout, stderr = ssh.exec_command("sudo service quagga restart")
		data=stdout.readlines()
		print "Configured Quagga"
		print

if __name__ == '__main__':
	configure_nodes()



