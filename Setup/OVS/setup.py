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

import json
import os
import paramiko
import getpass
import sys

def copy_files(ssh,path):
	stdin, stdout, stderr = ssh.exec_command("sudo cp -rf "+path+"/* /var/www/html/")
	data=stdout.readlines()

def init_database(ssh):
        stdin, stdout, stderr = ssh.exec_command("sudo python /var/www/html/SENSS/Setup/OVS/init.py")
        data=stdout.readlines()

def install_dependencies(ssh,path):
        stdin, stdout, stderr = ssh.exec_command("sudo service quagga stop")
        data=stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command(path+"/SENSS/Setup/OVS/install_dependencies.sh")
        data=stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command("cd /var/www/html/SENSS/Setup/Netronome/ryu/ryu-master; sudo python /var/www/html/SENSS/Setup/Netronome/ryu/ryu-master/setup.py install")
        data=stdout.readlines()
        print "Installed dependencies"

def start_ryu(ssh):
        stdin, stdout, stderr = ssh.exec_command("killall screen")
        data=stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command("screen -d -m ryu-manager /var/www/html/SENSS/ryu/ryu-master/ryu/app/ofctl_rest.py")
        data=stdout.readlines()
        print "Started RYU controller"

def start_monitoring(ssh):
        stdin, stdout, stderr = ssh.exec_command("screen -d -m sudo python /var/www/html/SENSS/UI_client_server/Client/direct_floods.py")
        data=stdout.readlines()
        print "Started Monitoring flows controller"


f=open("config","r")
config={}
for line in f:
	config[line.strip().split(",")[0]]=line.strip().split(",")[1]
f.close()


type=sys.argv[1]

username=raw_input("Username: ").strip()
password=getpass.getpass()

#Install and Start RYU
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(config["controller_ip"],username=username, password=password,timeout=30)
copy_files(ssh,config["path"])
init_database(ssh)
install_dependencies(ssh,config["path"])
start_ryu(ssh)
start_monitoring(ssh)



ip_dict={}
file_to_read=open("quagga_input","r")
for line in file_to_read:
        line=line.strip().split("qwerty123")
        ip=line[0]
        value=json.loads(line[1])
        ip_dict[ip]=value
file_to_read.close()

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
controller_ip=config["controller_ip"]
list_of_cities=sorted(list_of_cities)
print list_of_cities
not_finished=[]
skipped=0
done_count=0
for switch in switches:
        #Script for the switch
        try:
                        url="i"+str(switch)+"."+config["exp_name"]+"."+config["proj_name"]
                        print url
                        command_to_execute="sudo python /var/www/html/SENSS/Setup/OVS/switch.py "+controller_ip+" "+switch
                        print url,command_to_execute
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(url,username=username, password=password,timeout=30)
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)
                        print ssh_stdout.readlines()
                        done_count=done_count+1
                        print done_count,len(switches)
                        print
        except Exception as e:
                not_finished.append(url)
                print "There is an exception",e
                a=1



not_finished=[]
done_count=0
for city in list_of_cities:
        print "Setting up Quagga for ",city," .."
        try:
                url="i"+str(list_of_cities.index(city)+1)+"."+config["exp_name"]+"."+config["proj_name"]
                command_to_execute="sudo python /var/www/html/SENSS/Setup/OVS/quagga.py "+city
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(url,username=username, password=password, timeout=360)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)
                print ssh_stdout.readlines()
		if type=="large":
			command_to_execute="sudo python /var/www/html/SENSS/Setup/OVS/docker_setup.py -n 200 -s 172."+str(i)+".0.1/16"
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command_to_execute)
                        print ssh_stdout.readlines()
                done_count=done_count+1
                print done_count,len(list_of_cities)
                print
        except:
                not_finished.append(url)
                done_count=done_count+1

