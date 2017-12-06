import urllib2,urllib
import os
import time
import sys
import subprocess
import json

condition_to_break=False

#Arguments to give 
# 1) Controller IP
# 2) Name of the city

while True:
	controller_ip=sys.argv[1]
	city_name=sys.argv[2]
	#cmd_to_execute='sudo dpkg -i /proj/SENSS/python-netifaces_0.6-2ubuntu1_amd64.deb'
	#cmd_to_execute='sudo dpkg -i /proj/SENSS/python-netifaces_0.8-3build1_i386.deb'

	cmd_to_execute='sudo apt-get install --assume-yes python-netifaces'
	proc = subprocess.Popen(cmd_to_execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	import netifaces

	interface_list = netifaces.interfaces()
	new_interface_list=[]

	for interface in interface_list:
		print interface
        	try:
                	address=netifaces.ifaddresses(interface)
			ip_addresses=[]
			for key,value in address.iteritems():
				for ips in value:
					if ":" not in ips["addr"]:
						test=ips["addr"].split(".")[0]
						if int(test)==10:
							new_interface_list.append(interface)

        	except Exception as e:
			print e
			a=1

	print "Got the interface list",new_interface_list

	cmd_to_execute="sudo ovs-vsctl del-br br0"
	proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	print "Delted Bridge br0"
	
	cmd_to_execute="sudo apt-get --assume-yes remove openvswitch-switch"
	proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	print "Removed OpenVswitch"
	
	cmd_to_execute="sudo apt-get update && sudo apt-get --assume-yes install openvswitch-switch"
	proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	print "Installed OpenVSwitch"

	method = "GET"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	request = urllib2.Request("http://"+controller_ip+":8080/stats/switches")
	request.get_method = lambda: method
	connection = opener.open(request)
	dpid_before = eval(connection.read())
	print "Got DPID Before",dpid_before

	cmd_to_execute="sudo ovs-vsctl add-br br0"
	proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	print "Added Bridge"


	cmd_to_execute="sudo ovs-vsctl set Bridge br0 protocols=OpenFlow13"
	proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	print "Added the protocol to be OpenFlow13"

	cmd_to_execute="sudo ovs-vsctl set-controller br0 tcp:"+controller_ip+":6633"
	proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	print "Attached Bridge to the Controller"
	
	for interface in new_interface_list:
		cmd_to_execute="sudo ovs-vsctl add-port br0 "+interface
		proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		proc.wait()

	while True:
		process = subprocess.Popen(['sudo', 'ovs-vsctl','show'], stdout=subprocess.PIPE)
		ovs_output, err = process.communicate()
		if "true" in ovs_output:
			break

	print "Verified that OVS is installed"

	method = "GET"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	request = urllib2.Request("http://"+controller_ip+":8080/stats/switches")
	request.get_method = lambda: method
	connection = opener.open(request)
	dpid_after = eval(connection.read())



	dpid= list(set(dpid_after)-set(dpid_before))[0]
	print "Switch DPID is",dpid
	port_list=[]

	method = "GET"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	request = urllib2.Request("http://"+controller_ip+":8080/stats/portdesc/"+str(dpid))
	request.get_method = lambda: method
	connection = opener.open(request)
	port_desc = eval(connection.read())

	for key,value in port_desc.iteritems():
		for port in value:
			if int(port["port_no"]<10):
				port_list.append(int(port["port_no"]))

	data_to_send={'dpid': int(dpid),'priority':0,'match':{'in_port':port_list[0]},'actions':[{'type':'OUTPUT','port': port_list[1]}]}
	method = "POST"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
	request.add_header("Content-Type",'application/json')
	request.get_method = lambda: method
	connection = opener.open(request)
	data = connection.read()

	data_to_send={'dpid': int(dpid),'priority':0,'match':{'in_port':port_list[1]},'actions':[{'type':'OUTPUT','port': port_list[0]}]}
	method = "POST"	
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
	request.add_header("Content-Type",'application/json')
	request.get_method = lambda: method
	connection = opener.open(request)
	data = connection.read()
	print "Added Flows"

	method = "GET"
	handler = urllib2.HTTPHandler()
	opener = urllib2.build_opener(handler)
	request = urllib2.Request("http://"+controller_ip+":8080/stats/flow/"+str(dpid))
	request.get_method = lambda: method	
	connection = opener.open(request)


	data=eval(connection.read())	
	print data
	print
	print len(data[str(dpid)])
	
	if len(data[str(dpid)]) == 2:
		condition_to_break=True
	print "Condition to break",condition_to_break
	if condition_to_break==True:
		#cmd_to_execute="sudo ovs-vsctl show"
		#proc = subprocess.Popen(cmd_to_execute,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		#proc.wait()
		#if "br0" in proc.stdout.readline():
		#	print "Done Setting Up Switch"
		#	break
		#print proc.stdout.readline()
		dpid_to_write=open("/proj/SENSS/DHS/Setup/Switch_DPID","a")
		dpid_to_write.write(str(dpid)+","+city_name+"\n")
		dpid_to_write.close()
		break
