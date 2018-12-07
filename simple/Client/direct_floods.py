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

import MySQLdb
import os
import json
import urllib2
import time
import pydot
active_senss_list=["3a50","14a28","17a18","9a81"]
dpid_to_senss={"3a50":"3","14a28":"14","17a18":"18","9a81":"81"}
senss_nodes=[3,14,18,81]
legit_nodes=[30,62]
attack_nodes=[73,84,76,33,7,44,63]
isp_names={}
font_size="10"
short={}
proxy_node=20
f=open("list_of_cities","r")
for line in f:
	short[line.strip().split("-")[0]]=line.strip().split("-")[1]
f.close()
f=open("asn_name","r")
for line in f:
	isp_names[short[line.strip().split(",")[0]]]=line.strip().split(",")[1]
	#isp_names[short[line.strip().split(",")[0]]]=short[line.strip().split(",")[0]]
f.close()
switch_to_isp={"i10a13":"ISP13","i11a14":"ISP14","i12a15":"ISP15","i14a8":"ISP8","i15a3":"ISP3","i15a4":"ISP4","i5a6":"ISP6","i5a7":"ISP7","i6a11":"ISP11","i6a9":"ISP9","i7a10":"ISP10","i9a12":"ISP12"}
dpid_dict={}
switch_dpid={}
f=open("active_senss","r")
for line  in f :
	dpid_dict[line.strip().split(",")[1]]=line.strip().split(",")[0]
	switch_dpid[line.strip().split(",")[0]]=line.strip().split(",")[1]
	active_senss[line.strip().split(",")[1]]=1
	dpid_isp[line.strip().split(",")[1]]=line.strip().split(",")[0]
f.close()
active_senss={}
dpid_isp={}

dpid_data={}
password="usc558l"
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
 	#total_times=int(item[3])
 	total_times=0
 	tag=item[4]
 	while True:
		sss=time.time()
		ty=[]
		for key,value in active_senss.iteritems():
    			if int(value)==1 or int(value)==0:
				method="GET"	
				anv=time.time()
				handler=urllib2.HTTPHandler()
				opener = urllib2.build_opener(handler)	
				if dpid_dict[key]=="106":
					dpid="106"
					dpid_data[dpid]={}
					dpid_data[dpid]["previous_count"]=0
					dpid_data[dpid]["diff"]=0
					continue

				url="http://localhost:8080/stats/flow/"+str(dpid_dict[key])
				#print url
				to_send={}
				request = urllib2.Request(url,data=json.dumps(to_send))
				request.add_header("Content-Type",'application/json')
				request.get_method = lambda: method	
				connection = opener.open(request)
				data = json.loads(connection.read())
				dpid=str(dpid_dict[key])
				if dpid not in dpid_data:
					dpid_data[dpid]={}
					dpid_data[dpid]["previous_count"]=0
					dpid_data[dpid]["diff"]=0
				try:
					dpid_data[dpid]["diff"]=data[dpid][1]["byte_count"]+data[dpid][0]["byte_count"]-dpid_data[dpid]["previous_count"]
					dpid_data[dpid]["previous_count"]=data[dpid][1]["byte_count"]+data[dpid][0]["byte_count"]
				except:
					continue
				ty.append(time.time()-anv)
				if time.time()-anv>=0.4:
					time.sleep(0.01)
					print "Sleeping"
		
		#print "Here",time.time()-sss,max(ty),sum(ty)/float(len(ty))


		results={}
		attack_path=[]
		zero_path=[]
		key_list=[]
		max_key=0
		max_key_value=0
		for key,value in dpid_data.iteritems():
			key_list.append(key)
			if dpid_data[key]["diff"]>=60000:
				t=switch_dpid[key].split("a")
				attack_path.append(str(t[0])+","+str(t[1]))
			if dpid_data[key]["diff"]<=10000:
				t=switch_dpid[key].split("a")
				zero_path.append(str(t[0])+","+str(t[1]))
			
			if switch_dpid[key] in active_senss_list:
				results[key]={}
				results[key]["DPID"]=key
				for key_1,value_1 in dpid_dict.iteritems():
					if value_1==key:
						break
				results[key]["ISP"]=isp_names[dpid_to_senss[switch_dpid[key]]]
				results[key]["Mark"]="False"
				if dpid_data[key]["diff"]>=60000:
				#if dpid_data[key]["diff"]>=72408533:
					results[key]["Mark"]="True"
					print dpid_data[key]["diff"]
					if dpid_data[key]["diff"]>=max_key_value:
						max_key=key
						max_key_value=dpid_data[key]["diff"]
				results[key]["Diff"]=dpid_data[key]["diff"]

		print
		print max_key_value,max_key

		print "Attack Path",attack_path
		#Parsing attack path
		attack_path_dict={}
		for path in attack_path:
			path_1=int(path.split(",")[0])
			path_2=int(path.split(",")[1])
			if path_1 not in attack_path_dict:
				attack_path_dict[path_1]=0
			if path_2 not in attack_path_dict:
				attack_path_dict[path_2]=0
			attack_path_dict[path_1]=attack_path_dict[path_1]+1
			attack_path_dict[path_2]=attack_path_dict[path_2]+1
		sources=[]
		attack=True
		for key,value in attack_path_dict.iteritems():
			if value==1 and key!=60:
				if key in senss_nodes:
					attack=False
					continue
				sources.append(isp_names[str(key)])
		print sources,attack
		#print "Zero Path",zero_path
		#time.sleep(o_time)
		#continue
		#if "21,45" in zero_path:
		#	print "Present in ZEROO"
		result_dict=json.dumps(results)
		#print "RESULTS",result_dict
		time_now=str(time.ctime())
		##Commenting for Houston
		#cur.execute("INSERT INTO SENSS_LOGS(ID,REQUEST_TYPE,REQUEST_FROM ,REQUEST_TO,OUTPUT,TIME)VALUES(0,'traffic_query','LBMC','LBMC','"+result_dict+"','"+time_now+"')")
		#f=open("/proj/SENSS/DHS/Proxy/proxy_file","r")
		proxy=0
		#for line in f:
		#	if "y" in line.strip():
		if results["232"]["Diff"]>=1000000:
				print "Turn on Proxy",results["232"]["Diff"]
				proxy=1
		f.close()
		proxy=str(proxy)
                cmd="UPDATE DIRECT_FLOODS SET RESULT='"+result_dict+"'WHERE ID="+str(request_id)
                cur.execute(cmd)
		if len(sources)!=0 and attack==True:
                	cmd="UPDATE DIRECT_FLOODS SET ATTACK='1',ATTACK_FROM='"+",".join(sources)+"'WHERE ID="+str(request_id)
                	cur.execute(cmd)
		if len(sources)==0 or attack==False:
                	cmd="UPDATE DIRECT_FLOODS SET ATTACK='0' WHERE ID="+str(request_id)
                	cur.execute(cmd)
                cmd="UPDATE DIRECT_FLOODS SET PROXY='"+proxy+"'WHERE ID="+str(request_id)
		cur.execute(cmd)
                db.commit()





		f=open("routing_table","r")
		graph = pydot.Dot(graph_type='graph', rankdir='BT',ranksep="0.9",nodesep="0.9", overlap="scale",ratio="auto")
		#graph = pydot.Dot(graph_type='graph')
		done_set=set()
		for line in f:
        		value=line.strip().split()
        		temp=value[::-1]
        		path= value[(len(value)-temp.index("0")):][:-1]
        		#if "72" in path or "39" in path or "1" in path or "14" in path or "56" in path or "":
        		if  "39" in path or "1" in path or "14" in path or "56" in path or "27" in path:
                		for i in range(0,len(path)-1):
		                        if path[i+1]+","+path[i] in done_set or path[i]+","+path[i+1] in done_set:
                		                continue
                        		if int(path[i])>int(path[i+1]):
                                		done_set.add(path[i]+","+path[i+1])
                        		else:
                                		done_set.add(path[i+1]+","+path[i])

                        		if int(path[i]) > int(path[i+1]):
                                		token=str(path[i+1])+","+str(path[i])
                        		else:
                                		token=str(path[i])+","+str(path[i+1])


                        		if int(path[i]) in senss_nodes or int(path[i+1]) in senss_nodes:
                                		if int(path[i]) in senss_nodes:
                                        		node_to_consider=path[i]
                                        		other_node=path[i+1]
                                		else:
                                        		node_to_consider=path[i+1]
                                        		other_node=path[i]
                                	
						if int(node_to_consider) > int(other_node):
                                        		token=str(other_node)+","+str(node_to_consider)
                                		else:
                                        		token=str(node_to_consider)+","+str(other_node)

		                                temp_node_1=pydot.Node(str(isp_names[node_to_consider]),style="filled",fillcolor="#cc99cc")
		                                temp_node_2=pydot.Node(str(isp_names[other_node]))
						
                		                graph.add_node(temp_node_1)
                		                graph.add_node(temp_node_2)
                                		if token in attack_path:
			 				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							print token
							if (token=="1,18" or token=="17,18")  and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							#if token=="17,18" and proxy=="1":
							#	print "Here 123456"
			 				#	edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="5")
                                			graph.add_edge(edge)
							continue
                                		if token in zero_path:
							#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				#edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")
                                			graph.add_edge(edge)
							continue
						else:
                        				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge=pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")
                                			graph.add_edge(edge)
						continue


                        		if int(path[i]) in attack_nodes:
						if int(path[i])==33:
                                			temp_node_1=pydot.Node(str(isp_names[path[i]]))
						else:
                                			temp_node_1=pydot.Node(str(isp_names[path[i]]))

						temp_node_2=pydot.Node(isp_names[path[i+1]])
                                		graph.add_node(temp_node_1)
                                		graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:
	                               			#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge=pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                                		if token in attack_path:
                                			#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")                                		
							if (token=="1,18" or token=="1,60") and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")
							else:
	                             				edge=pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")
				   		if token in zero_path:
			 				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                               	 		continue

                        		if int(path[i+1]) in attack_nodes:
						if int(path[i+1])==33:
                                			temp_node_1=pydot.Node(str(isp_names[path[i+1]]))
						else:
                                			temp_node_1=pydot.Node(str(isp_names[path[i+1]]))

						temp_node_2=pydot.Node(isp_names[path[i]])

                                		graph.add_node(temp_node_1)
                                		graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:
                               				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge=pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                                		if token in attack_path:
                                			#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if token=="1,60":
								print "Here 2"

							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
								edge=pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")
                                		if token in zero_path:	
							#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                               	 		continue

                        		if int(path[i]) in legit_nodes:
                                		temp_node_1=pydot.Node(str(isp_names[path[i]]))
						temp_node_2=pydot.Node(isp_names[path[i+1]])

                                		graph.add_node(temp_node_1)
						graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:
        	               				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")
	
                                		if token in attack_path:
                        				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if token=="1,60":
								print "Here 2"

							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
				 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                                		if token in zero_path:
			 				edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                                		continue
                        		if int(path[i+1]) in legit_nodes:
                                		temp_node_1=pydot.Node(str(isp_names[path[i+1]]))
                                		graph.add_node(temp_node_1)
						temp_node_2=pydot.Node(isp_names[path[i]])
						graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:
	                       				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")
                                		if token in attack_path:
                        				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
				 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")
                                		if token in zero_path:
			 				edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                                		continue

					temp_node_1=pydot.Node(isp_names[path[i]])
					temp_node_2=pydot.Node(isp_names[path[i+1]])

                        		if token in attack_path:
                                		#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
						if token=="1,60":
							print "Here 2"

						if (token=="1,18" or token=="1,60") and proxy=="1":
							print "Here"
			 				edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
						if token=="17,18" and proxy=="1":
		 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

						else:
		 					edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                			if token in zero_path:
						edge=pydot.Edge(temp_node_1,temp_node_2,splines="true") 

		      		 	if token not in attack_path and token not in zero_path:
                                		#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
						edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                        		graph.add_edge(edge)		
		f.close()
		node_sixty=pydot.Node(isp_names["60"],style="filled", fillcolor="#cfd2da",penwidth="5")
		graph.add_node(node_sixty)
		temp_node=pydot.Node(isp_names["39"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge = pydot.Edge(node_sixty,temp_node,splines="True",color="green",penwidth="4")
		if "39,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "39,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,fontsize="10",splines="true")
		graph.add_edge(edge)

		temp_node=pydot.Node(isp_names["1"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge = pydot.Edge(node_sixty,temp_node,splines="True",color="green",penwidth="4")
		if "1,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			if proxy=="1":
				edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="12")
			else:
				edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "1,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,fontsize="10",splines="true")
		graph.add_edge(edge)

		temp_node=pydot.Node(isp_names["56"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge = pydot.Edge(node_sixty,temp_node,splines="True",color="green",penwidth="4")

		if "56,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "56,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,fontsize="10",splines="true")
		graph.add_edge(edge)


		temp_node=pydot.Node(isp_names["27"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge = pydot.Edge(node_sixty,temp_node,splines="True",color="green",penwidth="4")

		if "27,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "27,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true")
		graph.add_edge(edge)

		temp_node=pydot.Node(isp_names["14"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge = pydot.Edge(node_sixty,temp_node,splines="True",color="green",penwidth="4")

		if "14,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "14,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true")

		graph.add_edge(edge)

		os.system("sudo rm ../demo.png")
 		graph.write_png('../demo.png')
 		#for key,value in results.iteritems():
		#	print key,value






		f=open("pidemo_2","r")
		graph = pydot.Dot(graph_type='graph', rankdir='BT',ranksep="0.9",nodesep="0.9", overlap="scale",ratio="auto")
		#graph = pydot.Dot(graph_type='graph')
		done_set=set()
		for line in f:
        		value=line.strip().split()
        		temp=value[::-1]
        		path= value[(len(value)-temp.index("0")):][:-1]
        		#if "72" in path or "39" in path or "1" in path or "14" in path or "56" in path or "":
        		if  "39" in path or "1" in path or "14" in path or "56" in path or "27" in path:
                		for i in range(0,len(path)-1):
		                        if path[i+1]+","+path[i] in done_set or path[i]+","+path[i+1] in done_set:
                		                continue
                        		if int(path[i])>int(path[i+1]):
                                		done_set.add(path[i]+","+path[i+1])
                        		else:
                                		done_set.add(path[i+1]+","+path[i])

                        		if int(path[i]) > int(path[i+1]):
                                		token=str(path[i+1])+","+str(path[i])
                        		else:
                                		token=str(path[i])+","+str(path[i+1])


                        		if int(path[i]) in senss_nodes or int(path[i+1]) in senss_nodes:
                                		if int(path[i]) in senss_nodes:
                                        		node_to_consider=path[i]
                                        		other_node=path[i+1]
                                		else:
                                        		node_to_consider=path[i+1]
                                        		other_node=path[i]
                                	
						if int(node_to_consider) > int(other_node):
                                        		token=str(other_node)+","+str(node_to_consider)
                                		else:
                                        		token=str(node_to_consider)+","+str(other_node)

		                                temp_node_1=pydot.Node(str(isp_names[node_to_consider]),style="filled",fillcolor="#cc99cc")
						if int(other_node)==proxy_node and proxy=="1":
			                                temp_node_2=pydot.Node(str(isp_names[other_node]),style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
		                                	temp_node_2=pydot.Node(str(isp_names[other_node]))
						
                		                graph.add_node(temp_node_1)
                		                graph.add_node(temp_node_2)
                                		if token in attack_path:
							if (token=="1,18" or token=="17,18") and proxy=="1":
								print "Here 1234"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")

							else:
				 				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
								edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")
                                			graph.add_edge(edge)
							continue
                                		if token in zero_path:
							edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")
                                			graph.add_edge(edge)
							continue
						else:
                        				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                                			graph.add_edge(edge)
						continue


                        		if int(path[i]) in attack_nodes:
						if int(path[i])==33:
                                			temp_node_1=pydot.Node(str(isp_names[path[i]]))
						else:
                                			if int(path[i])==proxy_node and proxy=="1":
								temp_node_1=pydot.Node(str(isp_names[path[i]]),style="filled",fillcolor="#cfd2da",penwidth="5")
							else:
								temp_node_1=pydot.Node(str(isp_names[path[i]]))

						if int(path[i+1])==proxy_node and proxy=="1":
							temp_node_2=pydot.Node(isp_names[path[i+1]],style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
							temp_node_2=pydot.Node(isp_names[path[i+1]])
                                		graph.add_node(temp_node_1)
                                		graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:

	                               			#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
								edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")


                                		if token in attack_path:
                                			#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")                                		
							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
								edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                                		if token in zero_path:
			 				edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                               	 		continue

                        		if int(path[i+1]) in attack_nodes:
						if int(path[i+1])==33:
                                			temp_node_1=pydot.Node(str(isp_names[path[i+1]]))
						else:
							if int(path[i+1])==proxy_node and proxy=="1":
			                       			temp_node_1=pydot.Node(str(isp_names[path[i+1]]),style="filled",fillcolor="#cfd2da",penwidth="5")
        						else:
		                        			temp_node_1=pydot.Node(str(isp_names[path[i+1]]))

						if int(path[i])==proxy_node and proxy=="1":
							temp_node_2=pydot.Node(isp_names[path[i]],style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
							temp_node_2=pydot.Node(isp_names[path[i]])

                                		graph.add_node(temp_node_1)
                                		graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:
                               				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                                		if token in attack_path:
                                			#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
								edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                                		if token in zero_path:	

							edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                               	 		continue

                        		if int(path[i]) in legit_nodes:
						if int(path[i])==proxy_node and proxy=="1":
	                                		temp_node_1=pydot.Node(str(isp_names[path[i]]),style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
                                			temp_node_1=pydot.Node(str(isp_names[path[i]]))
						
						if int(path[i+1])==proxy_node and proxy=="1":
							temp_node_2=pydot.Node(isp_names[path[i+1]],style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
							temp_node_2=pydot.Node(isp_names[path[i+1]])

                                		graph.add_node(temp_node_1)
						graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:

        	               				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                                		if token in attack_path:
                        				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
								edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                                		if token in zero_path:
			 				edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                                		continue
                        		if int(path[i+1]) in legit_nodes:
						if int(path[i+1])==proxy_node and proxy=="1":
	                                		temp_node_1=pydot.Node(str(isp_names[path[i+1]]),style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
        	                        		temp_node_1=pydot.Node(str(isp_names[path[i+1]]))
                                		graph.add_node(temp_node_1)
						if int(path[i])==proxy_node and proxy=="1":
							temp_node_2=pydot.Node(isp_names[path[i]],style="filled",fillcolor="#cfd2da",penwidth="5")
						else:
							temp_node_2=pydot.Node(isp_names[path[i]])
						graph.add_node(temp_node_2)
						if token not in attack_path and token not in zero_path:

	                       				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                                		if token in attack_path:
                        				#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
							if (token=="1,18" or token=="1,60") and proxy=="1":
								print "Here"
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
							if token=="17,18" and proxy=="1":
			 					edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

							else:
								edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                                		if token in zero_path:
			 				edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',splines="true")
			 				edge = pydot.Edge(temp_node_1,temp_node_2,splines="true")

                                		graph.add_edge(edge)
                                		continue

					if int(path[i])==proxy_node and proxy=="1":
						temp_node_1=pydot.Node(isp_names[path[i]],style="filled",fillcolor="#cfd2da",penwidth="5")
					else:
						temp_node_1=pydot.Node(isp_names[path[i]])
					if int(path[i+1])==proxy_node and proxy=="1":
						temp_node_2=pydot.Node(isp_names[path[i+1]],style="filled",fillcolor="#cfd2da",penwidth="5")
					else:
						temp_node_2=pydot.Node(isp_names[path[i+1]])
						
					graph.add_node(temp_node_1)	
					graph.add_node(temp_node_2)	
                        		if token in attack_path:
                                		#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
						if (token=="1,18" or token=="1,60") and proxy=="1":
							print "Here"
			 				edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="12")
						if token=="17,18" and proxy=="1":
							edge = pydot.Edge(temp_node_1,temp_node_2,color="red",penwidth="7")

						else:
							edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="red",penwidth="5")

                			if token in zero_path:
						edge=pydot.Edge(temp_node_1,temp_node_2,splines="true") 
		      		 	if token not in attack_path and token not in zero_path:
                                		#edge = pydot.Edge(temp_node_1,temp_node_2,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',splines="true")
						edge = pydot.Edge(temp_node_1,temp_node_2,splines="true",color="green",penwidth="4")

                        		graph.add_edge(edge)		
		f.close()
		#node_sixty=pydot.Node(isp_names["60"],style="filled", fillcolor="#cfd2da",penwidth="5")
		node_sixty=pydot.Node(isp_names["60"],style="filled", fillcolor="#FFFF00",penwidth="5")
		graph.add_node(node_sixty)
		temp_node=pydot.Node(isp_names["39"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge= pydot.Edge(node_sixty,temp_node,splines="true",color="green",penwidth="4")
		if "39,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "39,60" in zero_path:
			edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,fontsize="10",splines="true")
		graph.add_edge(edge)

		temp_node=pydot.Node(isp_names["1"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge= pydot.Edge(node_sixty,temp_node,splines="true",color="green",penwidth="4")

		if "1,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			if proxy=="1":
				edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="12")
			else:
				edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "1,60" in zero_path:
			edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,fontsize="10",splines="true")
		graph.add_edge(edge)

		temp_node=pydot.Node(isp_names["56"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge= pydot.Edge(node_sixty,temp_node,splines="true",color="green",penwidth="4")

		if "56,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "56,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,fontsize="10",splines="true")
		graph.add_edge(edge)


		temp_node=pydot.Node(isp_names["27"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge= pydot.Edge(node_sixty,temp_node,splines="true",color="green",penwidth="4")

		if "27,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "27,60" in zero_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true")
		graph.add_edge(edge)

		temp_node=pydot.Node(isp_names["14"])
		graph.add_node(temp_node)
		#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/half_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
		edge= pydot.Edge(node_sixty,temp_node,splines="true",color="green",penwidth="4")

		if "14,60" in attack_path:
			#edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/full_1.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true",color="red",penwidth="5")

                if "14,60" in zero_path:
			edge = pydot.Edge(node_sixty,temp_node,label = '<<table border="0"><tr><td><img src="/users/satyaman/zero.png" scale="BOTH"/></td></tr></table>>',fontsize="10",splines="true")
			edge = pydot.Edge(node_sixty,temp_node,splines="true")

		graph.add_edge(edge)

		os.system("sudo rm demo_proxy.png")
 		graph.write_png('demo_proxy.png')
 		#for key,value in results.iteritems():
		#	print key,value

		print "Wrote"
		print
 		time.sleep(o_time)
	
