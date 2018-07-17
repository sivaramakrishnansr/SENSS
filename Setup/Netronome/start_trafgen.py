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
	if type=="ddos":
	        f=open("nodes_ddos_with_sig","r")
	if type=="alpha":
		f=open("nodes_ddos_without_sig","r")

        for line in f:
		if len(line.strip())==0:
			continue
                if "#" in line:
                        continue
			
		if type=="proxy" or type=="ddos":
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

		if type=="alpha":
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
	#password=getpass.getpass()
	password="kru!1dalahomora"
	for node in nodes:
                print "Node: ",node," "
		#if node =="hpc054" or node=="hpc039" or node=="hpc043":
		#if node!="hpc056":
		if True:
	                ssh = paramiko.SSHClient()
                	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        	        ssh.connect(node,username="satyaman", password=password, timeout=3)
                	#Patching netronome
			if type=="proxy" or type=="ddos":
				stdin,stdout,stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+nodes[node]["server_mac"]+" "+nodes[node]["server_ip"]+" "+nodes[node]["legit_traffic"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"]+" "+nodes[node]["legit_address"]) 
				print "sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+nodes[node]["server_mac"]+" "+nodes[node]["server_ip"]+" "+nodes[node]["legit_traffic"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"]+" "+nodes[node]["legit_address"]
			if type=="alpha":
				stdin,stdout,stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+nodes[node]["asn"]+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+ nodes[node]["server_mac"]+" "+nodes[node]["legit_sources"]+" "+nodes[node]["attack_sources"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"])
				print "sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/trafgen.py "+type+" "+nodes[node]["asn"]+" "+attack_ip+" "+str(nodes[node]["attack_duration"])+" "+nodes[node]["attack_rate"]+" "+nodes[node]["switch_mac"]+" "+ nodes[node]["server_mac"]+" "+nodes[node]["legit_sources"]+" "+nodes[node]["attack_sources"]+" "+nodes[node]["legit_traffic_rate"]+" "+nodes[node]["legit_traffic_duration"]


if __name__ == '__main__':
	start_attack()
