import sys
import json
import paramiko
import getpass
import socket
import urllib2
import subprocess

def start_attack():
        nodes=[]
        two_ports=[]
        f=open("attack_nodes","r")
        for line in f:
                if "#" in line:
                        continue
                node=line.strip().split(" ")[0]
                nodes.append(node)
        f.close()
	password=getpass.getpass()
	for node in nodes:
                print "Node: ",node," "
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(node,username="satyaman", password=password, timeout=3)
                #Patching netronome
		#nohup ./exec_name > /dev/null 2>&1 &\n
                stdin, stdout, stderr = ssh.exec_command("sudo -b /proj/SENSS/SENSS_git/SENSS/Setup/trafgen/trafgen.py")
                #data=stdout.readlines()	

if __name__ == '__main__':
	start_attack()
