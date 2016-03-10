
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
from time import strftime
import MySQLdb
import os
import json
import urllib2
import time
import pydot




def process(ip_dict):
	city_dict={"BocaRaton":9,"Stuart":44,"FtLauderdale":3,"DaytonaBeach":40,"Knoxville":5,"Chatanooga":6,"Biloxi":7,"Memphis":8,"Winston":182}
	password=""
	db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
	cur=db.cursor()
	cur.execute("USE SENSS")
	while True:
	 db.commit()
	 cur.execute("SELECT * FROM DIRECT_FLOODS")
	 for item in cur.fetchall():
		request_id=int(item[0])
		request_city=item[1]
		o_time=int(item[2])
		total_times=int(item[3])
		tag=item[4]
		method = "POST"
		handler = urllib2.HTTPHandler()
		opener = urllib2.build_opener(handler)
		iteration_count=0
		request_array=ip_dict[request_city]
		print request_array
		
		while True:
			graph = pydot.Dot(graph_type='digraph')

			node_dict={}
			node_dict[request_city]=pydot.Node(request_city, style="filled", fillcolor="red")
			cur.execute("SELECT RESULT FROM DIRECT_FLOODS WHERE ID="+str(request_id))
			for r in cur.fetchall():
				if r[0] is None:
					dict={}
				else:
					dict=json.loads(r[0])
			print "Before Insertion",dict			
			for item_1 in request_array:
				for dpid,cities in item_1.iteritems():
					temp_cities=cities.split("-")
					active_city=""
					if request_city == temp_cities[0]:
						active_city=temp_cities[1]
					else:
						active_city=temp_cities[0]
					if active_city=="Winston":
						node_dict[active_city]=pydot.Node(active_city+"(You)", style="filled", fillcolor="red")
					else:	
						node_dict[active_city]=pydot.Node(active_city, style="filled", fillcolor="red")

					method="POST"
					handler=urllib2.HTTPHandler()
					opener = urllib2.build_opener(handler)
					url="http://localhost:8080/stats/flow/"+str(dpid)
					to_send={}
					request = urllib2.Request(url,data=json.dumps(to_send))
					
					request.add_header("Content-Type",'application/json')
					request.get_method = lambda: method
    					connection = opener.open(request)
					data = json.loads(connection.read())
					byte_count=0
					packet_count=0

					for flow in data[dpid]:			
						byte_count=byte_count+int(flow["byte_count"])
						packet_count=packet_count+int(flow["packet_count"])

					if active_city not in dict:
						dict[active_city]={}
						dict[active_city]["Byte Count"]=0
						dict[active_city]["Packet Count"]=0
						dict[active_city]["Last Packet Count"]=0
						dict[active_city]["Last Byte Count"]=0
						dict[active_city]["DPID"]=dpid
						dict[active_city]["Mark"]="False"
					
					if True:
						if packet_count==byte_count==0:
							dict[active_city]["Packet Count"]=0
        	                                        dict[active_city]["Byte Count"]=0
						else:
							dict[active_city]["Packet Count"]=packet_count-dict[active_city]["Last Packet Count"]
                                                	dict[active_city]["Byte Count"]=byte_count-dict[active_city]["Last Byte Count"]
						dict[active_city]["Last Packet Count"]=packet_count
						dict[active_city]["Last Byte Count"]=byte_count
						if active_city=="Winston":
							print dict[active_city]
                                                bandwidth_percentage=round((dict[active_city]["Byte Count"]/(float(o_time)*1024*1024*0.23))*100,2)

					result=json.dumps(dict)
									
			total_byte=0
			flag=False
			traffic_percent=0
			for active_city,value in dict.iteritems():
				if active_city != "Winston":
					total_byte=total_byte+dict[active_city]["Byte Count"]
			for active_city,value in dict.iteritems():
				if active_city != "Winston" and total_byte!=0:
					traffic_percent=round((dict[active_city]["Byte Count"]/float(total_byte))*100,2)
					print "Winston",active_city,traffic_percent,"%"			
				if active_city!="Winston":
					if traffic_percent > 45 and dict[active_city]["Packet Count"] > 400:
                                                           graph.add_edge(pydot.Edge(node_dict[active_city],node_dict[request_city],label=str(traffic_percent)+"%",color="red"))
						           flag=True	
							   dict[active_city]["Mark"]="True"		
					else:
						           if dict[active_city]["Mark"]=="True":
								dict[active_city]["Mark"]="False"		
                                                           graph.add_edge(pydot.Edge(node_dict[active_city],node_dict[request_city],label=str(traffic_percent)+"%",color="blue"))

			if flag==True:
                        	graph.add_edge(pydot.Edge(node_dict[request_city],node_dict["Winston"],color="red"))
			else:
                        	graph.add_edge(pydot.Edge(node_dict[request_city],node_dict["Winston"],color="blue"))
			result=json.dumps(dict)
			cmd="UPDATE DIRECT_FLOODS SET RESULT='"+result+"' WHERE ID="+str(request_id)
			cur.execute(cmd)
			time_now=str(strftime("%Y-%m-%d %H:%M:%S"))
			request_type="traffic_query"
			request_from="Winston"
			cmd="INSERT INTO SENSS_LOGS (REQUEST_TYPE,REQUEST_FROM,TIME,RESPONSE)VALUES('"+request_type+"','"+request_from+"','"+time_now+"','"+result+"' )"
			print cmd
			print
			cur.execute(cmd)
			db.commit()
			print
			print
			os.system("sudo rm /var/www/html/graph.png")
			graph.write_png('/var/www/html/graph.png')
			time.sleep(o_time)


ip_dict={}
switch_dpid={}
file_to_read=open("/var/www/html/data/Switch_DPID")
for line in file_to_read:
	line=line.strip().split(",")
	switch_dpid[line[1]]=line[0]
file_to_read.close()


print switch_dpid
list_of_cities=set()
temp_ip_dict={}
file_to_read=open("/var/www/html/data/quagga_input","r")
for line in file_to_read:
        line=line.strip().split("qwerty123")
        ip=line[0]
        value=json.loads(line[1])
        temp_ip_dict[ip]=value
file_to_read.close()
for city,value in temp_ip_dict.iteritems():
	list_of_cities.add(city)

list_of_cities=sorted(list(list_of_cities))


file_to_read=open("/var/www/html/data/quagga_input","r")
for line in file_to_read:
        line=line.strip().split("qwerty123")
        ip=line[0]
        value=json.loads(line[1])
	for item in value:
		for ip_1,asn in item.iteritems():
			temp=ip_1.split(".")[1:3]
			if int(temp[0]) < int(temp[1]):
				switch=temp[0]+"a"+temp[1]
			else:
				switch=temp[1]+"a"+temp[0]
			if ip not in ip_dict:
				ip_dict[ip]=[]
			print switch
			v=list_of_cities[int(switch.split("a")[0])-1]+"-"+list_of_cities[int(switch.split("a")[1])-1]
			temp_dict={}
			temp_dict[switch_dpid[switch]]=v
        		ip_dict[ip].append(temp_dict)

file_to_read.close()
print ip_dict["Miami"]
print ip_dict["Jacksonville"]
print ip_dict["Atlanta"]
print ip_dict["NewOrleans"]
print ip_dict["PanamaCity"]
ip_dict["AT&T"]=[{'30': 'BocaRaton-AT&T'},{'42': 'AT&T-Stuart'}, {'121': 'FtLauderdale-AT&T'},{'148': 'DaytonaBeach-AT&T'},{'28': 'AT&T-Knoxville'},{'159': 'AT&T-Chatanooga'}, {'60': 'Biloxi-AT&T'}, {'16': 'Memphis-AT&T'},{'182': 'AT&T-Winston'}]
process(ip_dict)

