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

def install_dependencies(ssh):
	stdin, stdout, stderr = ssh.exec_command("/proj/SENSS/SENSS_git/SENSS/Setup/install_dependencies.sh")
	data=stdout.readlines()
	stdin, stdout, stderr = ssh.exec_command("cd /users/satyaman/ryu/ryu-master; sudo python /users/satyaman/ryu/ryu-master/setup.py install")
	data=stdout.readlines()	
	print "Installed dependencies"

def start_ryu(ssh):
	stdin, stdout, stderr = ssh.exec_command("killall screen")
	data=stdout.readlines()
	stdin, stdout, stderr = ssh.exec_command("screen -d -m ryu-manager /proj/SENSS/SENSS_git/SENSS/ryu/ryu-master/ryu/app/ofctl_rest.py")
	data=stdout.readlines()
	print "Started RYU controller"

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
        connection = opener.open(request)
        data = json.loads(connection.read())
	for item in data:
		dpid=item
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

def configure_nodes():
	nodes=[]
	two_ports=[]
	f=open("nodes","r")
	for line in f:
		if "#" in line:
			continue
		node=line.strip().split(" ")[0]
		number_of_ports=int(line.strip().split(" ")[1])
		nodes.append(node)
		if number_of_ports==2:
			two_ports.append(node)
	f.close()

	password=getpass.getpass()
	for node in nodes:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(node,username="satyaman", password=password, timeout=3)
		ip_1,ip_2,first_octet=return_ips(node)
		controller_ip=socket.gethostbyname(node)
		print "Node: ",node," "
		#Install dependencies
		install_dependencies(ssh)

		#Start RYU
		start_ryu(ssh)

		#Start OVS on netronome NIC
		start_ovs(ssh)

		#Add IP address to interface_1
		stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py -b nfp_netvf 08:08.0")
		data=stdout.readlines()
		interface_1=get_interface(ssh,"08:08.0")
		stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_1+" "+ip_1)
		data=stdout.readlines()

		#Setup OVS
		setup_ovs(ssh,"sdn_p0","sdn_v0.0",1,2,interface_1,False)

		#Add controller 
		stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl set-controller br0 tcp:"+controller_ip+":6633")
		data=stdout.readlines()

		if node in two_ports:
			#Add IP address to interface_2
			stdin, stdout, stderr = ssh.exec_command("sudo python /opt/netronome/libexec/dpdk_nic_bind.py -b nfp_netvf 08:08.1")
			data=stdout.readlines()
			interface_2=get_interface(ssh,"08:08.1")
			stdin, stdout, stderr = ssh.exec_command("sudo ifconfig "+interface_2+" "+ip_2)
			data=stdout.readlines()

			#Setup OVS
			setup_ovs(ssh,"sdn_p1","sdn_v0.1",3,4,interface_2,True)

		#Add rules
		dpid=get_dpid(controller_ip)
		add_forwarding_rules(controller_ip,dpid,1,2)
		add_forwarding_rules(controller_ip,dpid,2,1)
		if node in two_ports:
			add_forwarding_rules(controller_ip,dpid,3,4)
			add_forwarding_rules(controller_ip,dpid,4,3)
		print "Added OF rules "

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
		if node in two_ports:
			string_to_write=string_to_write+" neighbor "+first_octet+".1.0.2 remote-as 1000\n"
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



