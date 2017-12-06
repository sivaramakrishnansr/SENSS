import json
import os
import paramiko


#Change the Experiment Name
exp_name="wash"
ip_dict={}
file_to_read=open("quagga_input","r")
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
fw=open("Switch_DPID","w")
fw.close()
list_of_cities=list(list_of_cities)
controller_ip="192.168.0.72"
list_of_cities=sorted(list_of_cities)
print list_of_cities
not_finished=[]
skipped=0
done_count=0
for switch in switches:
	#Script for the switch
	try:
			url="i"+str(switch)+"."+exp_name+".senss"
			print url
			command_to_execute="sudo python /proj/SENSS/DHS/Setup/switch_setup.py "+controller_ip+" "+switch
			#command_to_execute="ls"
			print url,command_to_execute
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
			ssh.connect(url,username="satyaman", password="usc558l",timeout=30)
			ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)	
			print ssh_stdout.readlines()
			done_count=done_count+1
			print
			print done_count,len(switches)
			print
	except Exception as e:
		not_finished.append(url)
		print "There is an exception",e
		a=1
	print
	print
print
print
print
print not_finished
