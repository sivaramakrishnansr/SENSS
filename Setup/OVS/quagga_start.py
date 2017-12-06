import json
import sys
import os
import paramiko

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

list_of_cities=list(list_of_cities)
list_of_cities=sorted(list_of_cities)
not_finished=[]
done_count=0
for city in list_of_cities:
	print "Setting up Quagga for ",city," .."
	try:
		url="i"+str(list_of_cities.index(city)+1)+".wash.senss"
		command_to_execute="sudo python /proj/SENSS/DHS/Setup/quagga_setup.py "+city
		print url,command_to_execute
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		ssh.connect(url,username="satyaman", password="usc558l", timeout=360)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)	
		print ssh_stdout.readlines()
		done_count=done_count+1
		print done_count,len(list_of_cities)
		print
	except:
		not_finished.append(url)
		done_count=done_count+1

print
print
print
print not_finished
