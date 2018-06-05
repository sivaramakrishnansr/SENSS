import json
import socket
import paramiko
import urllib2
import sys
import getpass
import time

def init_database(ssh,nodes,is_client):
        stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/init.py usc558l")
        data=stdout.readlines()
        if is_client==1:
                return
        for node,node_data in nodes.iteritems():
                stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/insert_topo.py "+node+" "+node_data["links_to"]+" "+str(node_data["self"]))
                data=stdout.readlines()


def add_client_entries(ssh,as_name,server_url,links_to,self):
        stdin, stdout, stderr = ssh.exec_command("sudo python /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/insert_senss_client.py usc558l "+as_name+" "+server_url+" "+links_to+" "+self)
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
                if dpid!=0:
                        break
                time.sleep(3)
        return dpid

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

def copy_files(ssh):
        stdin, stdout, stderr = ssh.exec_command("sudo cp -rf /proj/SENSS/SENSS_git/* /var/www/html/")
        data=stdout.readlines()
        print "Copied files"

def start():
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
		print number_of_ports
                if number_of_ports==2:
                        two_ports.append(node)
        f.close()

        password=getpass.getpass()

        for node in nodes:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(node,username="satyaman", password=password, timeout=3)
                controller_ip=socket.gethostbyname(node)
                print "Node: ",node," ",controller_ip,node in two_ports
		#copy_files(ssh)
		if nodes[node]["node_type"]=="client":
                        init_database(ssh,nodes,1)
                else:
                        init_database(ssh,nodes,0)
                if nodes[node]["node_type"]=="client":
                        for node,values in nodes.iteritems():
                                self="0"
                                if values["node_type"]=="client":
                                        self="1"
                                add_client_entries(ssh,values["asn"],values["server_url"],values["links_to"],self)



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
			print "In one port"
                        stdin, stdout, stderr = ssh.exec_command("sudo sh /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/ovs_one_port.sh")
                        data=stdout.readlines()
			print data
                        #Add controller
			print controller_ip,"IP"
                        stdin, stdout, stderr = ssh.exec_command("sudo ovs-vsctl set-controller br0 tcp:"+controller_ip+":6633")
                        data=stdout.readlines()
			print data
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

start()
