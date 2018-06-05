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
	        f=open("nodes","r")
	if type=="ddos":
	        f=open("nodes_1","r")
        for line in f:
		if len(line.strip())==0:
			continue
                if "#" in line:
                        continue
		##hpc039 2 server hpc039 http://hpc039/SENSS/UI_client_server/Server/api.php hpc057 0 100 10
                node=line.strip().split(" ")[0]
                number_of_ports=int(line.strip().split(" ")[1])
                node_type=line.strip().split(" ")[2]
                asn=line.strip().split(" ")[3]
                server_url=line.strip().split(" ")[4]
                links_to=line.strip().split(" ")[5]
                self=int(line.strip().split(" ")[6])
		rate=line.strip().split(" ")[7]
		duration=int(line.strip().split(" ")[8])
		server_mac=line.strip().split(" ")[9]
		switch_mac=line.strip().split(" ")[10]
		server_ip=line.strip().split(" ")[11]
		legit_traffic=line.strip().split(" ")[12]
		legit_traffic_rate=line.strip().split(" ")[13]
		if node_type=="client":
			attack_ip=node.replace("hpc0","")+".0.0.1"
			continue
                nodes[node]={}
                nodes[node]["node_type"]=node_type
                nodes[node]["asn"]=asn
                nodes[node]["server_url"]=server_url
                nodes[node]["links_to"]=links_to
                nodes[node]["self"]=self
		nodes[node]["rate"]=rate
		nodes[node]["duration"]=duration
		nodes[node]["server_mac"]=server_mac
		nodes[node]["switch_mac"]=switch_mac
		nodes[node]["server_ip"]=server_ip
		nodes[node]["legit_traffic"]=legit_traffic
		nodes[node]["legit_traffic_rate"]=legit_traffic_rate
        f.close()
	password=getpass.getpass()
	for node in nodes:
                print "Node: ",node," "
		#if node =="hpc054" or node=="hpc039" or node=="hpc043":
		if node!="hpc056":
	                ssh = paramiko.SSHClient()
                	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	        ssh.connect(node,username="satyaman", password=password, timeout=3)
                	#Patching netronome
			#nohup ./exec_name > /dev/null 2>&1 &\n
                	#stdin, stdout, stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+attack_ip+" "+str(nodes[node]["duration"])+" "+nodes[node]["rate"])
			stdin,stdout,stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+attack_ip+" "+str(nodes[node]["duration"])+" "+nodes[node]["rate"]+" "+nodes[node]["switch_mac"]+" "+nodes[node]["server_mac"]+" "+nodes[node]["server_ip"]+" "+nodes[node]["legit_traffic"]+" "+nodes[node]["legit_traffic_rate"])
			print "sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+attack_ip+" "+str(nodes[node]["duration"])+" "+nodes[node]["rate"]+" "+nodes[node]["switch_mac"]+" "+nodes[node]["server_mac"]+" "+nodes[node]["server_ip"]+" "+nodes[node]["legit_traffic"]+" "+nodes[node]["legit_traffic_rate"]
	                #data=stdout.readlines()	

if __name__ == '__main__':
	start_attack()
