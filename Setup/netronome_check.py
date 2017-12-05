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

#nodes 53 55 45 are down
nodes=["hpc039","hpc041","hpc042","hpc043","hpc044","hpc046","hpc047","hpc048","hpc049","hpc050","hpc052","hpc054","hpc056","hpc057"]
nodes=["hpc049"]
node_status={}
for node in nodes:
	node_status[node]="FAIL"

two_ports=["hpc039","hpc041","hpc042","hpc043","hpc044","hpc046","hpc047"]

password=getpass.getpass()
for node in nodes:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(node,username="satyaman", password=password, timeout=3)


		



	#Install dependencies
	stdin, stdout, stderr = ssh.exec_command("/proj/SENSS/SENSS_git/SENSS/Setup/install_dependencies.sh")
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("cd /users/satyaman/ryu/ryu-master; sudo python /users/satyaman/ryu/ryu-master/setup.py install")
	for item in stdout.readlines():
		print item.strip()
	
	#Start RYU
	stdin, stdout, stderr = ssh.exec_command("killall screen")
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("screen -d -m ryu-manager /proj/SENSS/SENSS_git/SENSS/ryu/ryu-master/ryu/app/ofctl_rest.py")
	for item in stdout.readlines():
		print item.strip()
	#Stop NFP
	stdin, stdout, stderr = ssh.exec_command("sudo /opt/netronome/bin/ovs-ctl stop")
	for item in stdout.readlines():
		print item.strip()
	
	#Start NFP
	stdin, stdout, stderr = ssh.exec_command("sudo /opt/netronome/bin/ovs-ctl start")
	for item in stdout.readlines():
		print item.strip()
	#Add IP address to interface_1
	stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py -b nfp_netvf 08:08.0")
	for item in stdout.readlines():
		print item.strip()

	stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py --status")
	for item in stdout.readlines():
		if "08:08.0" in item.strip() and "if=eth" in item.strip():
			interface_1=item.strip().split(" ")[3].split("=")[-1]



	first_octet=node.replace("hpc0","")
	ip_1=first_octet+".0.0.1"
	ip_2=first_octet+".1.0.1"
	stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_1+" "+ip_1)
	for item in stdout.readlines():
		print item.strip()

	#Configure OVS
	stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl --if-exist del-br br0")
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command('sudo ovs-vsctl add-br br0 -- set Bridge br0 "protocols=OpenFlow13"')
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("sudo ovs-ofctl -O OpenFlow13 del-flows br0")
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("sudo ovs-ofctl -O OpenFlow13 del-groups br0 group_id=0")
	for item in stdout.readlines(): 
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl add-port br0 sdn_p0 -- set Interface sdn_p0 ofport_request=1")
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl add-port br0 sdn_v0.0 -- set Interface sdn_v0.0 ofport_request=2")
	for item in stdout.readlines():
		print item.strip()

	stdin, stdout, stderr = ssh.exec_command("ifconfig sdn_v0.0 up")
	for item in stdout.readlines():
		print item.strip()
	stdin, stdout, stderr = ssh.exec_command("ifconfig "+interface_1+" up")
	for item in stdout.readlines():
		print item.strip()

	#Adding the controller ip
	controller_ip=socket.gethostbyname(node)
	stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl set-controller br0 tcp:"+controller_ip+":6633")
	for item in stdout.readlines():
		print item.strip()

	if node in two_ports:
		stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py -b nfp_netvf 08:08.1")
		for item in stdout.readlines():
			print item.strip()

		stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py --status")
		for item in stdout.readlines():
			if "08:08.1" in item.strip() and "if=eth" in item.strip():
				interface_2=item.strip().split(" ")[3].split("=")[-1]

		stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_2+" "+ip_2)
		for item in stdout.readlines():
			print item.strip()

		stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl add-port br0 sdn_p1 -- set Interface sdn_p1 ofport_request=3")
		for item in stdout.readlines():
			print item.strip()
		stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl add-port br0 sdn_v0.1 -- set Interface sdn_v0.1 ofport_request=4")
		for item in stdout.readlines():
			print item.strip()
		stdin, stdout, stderr = ssh.exec_command("ifconfig sdn_v0.1 up")
		for item in stdout.readlines():
			print item.strip()

		stdin, stdout, stderr = ssh.exec_command("ifconfig "+interface_2+" up")
		for item in stdout.readlines():
			print item.strip()
		

	#Add rules
        method = "GET"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
	print "http://"+controller_ip+":8080/stats/switches"
        request = urllib2.Request("http://"+controller_ip+":8080/stats/switches")
        request.get_method = lambda: method
        connection = opener.open(request)
        data = json.loads(connection.read())
	for item in data:
		dpid=item

        data_to_send={'dpid': int(dpid),'priority':1,'match':{'in_port':1},'actions':[{'type':'OUTPUT','port':2}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()

        data_to_send={'dpid': int(dpid),'priority':1,'match':{'in_port':2},'actions':[{'type':'OUTPUT','port':1}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()

	if node in two_ports:
	        data_to_send={'dpid': int(dpid),'priority':1,'match':{'in_port':3},'actions':[{'type':'OUTPUT','port':4}]}
        	method = "POST"
        	handler = urllib2.HTTPHandler()
        	opener = urllib2.build_opener(handler)
        	request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        	request.add_header("Content-Type",'application/json')
        	request.get_method = lambda: method
        	connection = opener.open(request)
        	data = connection.read()

        	data_to_send={'dpid': int(dpid),'priority':1,'match':{'in_port':4},'actions':[{'type':'OUTPUT','port':3}]}
        	method = "POST"
        	handler = urllib2.HTTPHandler()
        	opener = urllib2.build_opener(handler)
        	request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
       	 	request.add_header("Content-Type",'application/json')
        	request.get_method = lambda: method
        	connection = opener.open(request)
        	data = connection.read()

	#Config zebra
	string_to_write="hostname zebra\n"
	string_to_write=string_to_write+"password en\n"
	string_to_write=string_to_write+"enable password en\n"
	string_to_write=string_to_write+"interface "+interface_1+"\n"
	string_to_write=string_to_write+" ip address "+ip_1+"/32\n"
	if node in two_ports:
		string_to_write=string_to_write+"interface "+interface_2+"\n"
		string_to_write=string_to_write+" ip address "+ip_2+"/32"

	stdin, stdout, stderr = ssh.exec_command("sudo rm /etc/quagga/zebra.conf")
	for item in stdout.readlines():
		print item.strip()

	stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /etc/quagga/zebra.conf")
	for item in stdout.readlines():
		print item.strip()


	string_to_write="zebra=yes\n"
	string_to_write=string_to_write+"bgpd=yes\n"
	string_to_write=string_to_write+"ospfd=no\n"
	string_to_write=string_to_write+"ospf6d=no\n"
	string_to_write=string_to_write+"ripd=no\n"
	string_to_write=string_to_write+"ripngd=no\n"
	string_to_write=string_to_write+"isisd=no\n"

	stdin, stdout, stderr = ssh.exec_command("sudo rm /etc/quagga/daemons")
	for item in stdout.readlines():
		print item.strip()

	stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /etc/quagga/daemons")
	for item in stdout.readlines():
		print item.strip()



	string_to_write="hostname "+node+"\n"
	string_to_write=string_to_write+"password en\n"
	string_to_write=string_to_write+"enable password en\n"
	string_to_write=string_to_write+"router bgp "+first_octet+"\n"
	string_to_write=string_to_write+" network "+first_octet+".0.0.0/8\n"
	string_to_write=string_to_write+" neighbor "+first_octet+".0.0.2 remote-as 1000\n"
	if node in two_ports:
		string_to_write=string_to_write+" neighbor "+first_octet+".1.0.2 remote-as 1000\n"
	stdin, stdout, stderr = ssh.exec_command("sudo rm /etc/quagga/bgpd.conf")
	for item in stdout.readlines():
		print item.strip()

	stdin, stdout, stderr = ssh.exec_command("echo '"+string_to_write+"' | sudo tee -a /etc/quagga/bgpd.conf")
	for item in stdout.readlines():
		print item.strip()
		
	stdin, stdout, stderr = ssh.exec_command("sudo service quagga restart")
	for item in stdout.readlines():
		print item.strip()


	
#ovs-ofctl -OOpenFlow13 show br0
#ovs-ofctl -OOpenFlow13 add-flow br0 in_port=1,actions=output:2
#ovs-ofctl -OOpenFlow13 add-flow br0 in_port=2,actions=output:1
#ovs-vsctl set Open_vSwitch . other_config:max-idle=-1


