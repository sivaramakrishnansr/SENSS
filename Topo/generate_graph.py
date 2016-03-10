
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
import sys
import json
import pydot

file_to_read=open(sys.argv[1],'r')
list_of_cities=[]
relation_list=[]
relation_dict={}
all_relation_list=[]
for line in file_to_read:
	if 'addSwitch' in line:
		city=line.strip().split('=')[0].strip()
		list_of_cities.append(city)	
	if 'addLink' in line and 'host' not in line and 'none' not in line and 'None' not in line:
		relation=line.strip().replace("self.addLink(","").replace(")","").replace(" ","").strip()
		all_relation_list.append(relation)
		relation=relation.split(',')[0:2]
		if relation[0] not in relation_dict:
			relation_dict[relation[0]]={}
			relation_dict[relation[0]]["Neighbours"]=[]
		relation_dict[relation[0]]["Neighbours"].append(relation[1])
		if relation[1] not in relation_dict:
			relation_dict[relation[1]]={}
			relation_dict[relation[1]]["Neighbours"]=[]
		relation_dict[relation[1]]["Neighbours"].append(relation[0])

list_of_cities=set()
for key,value in relation_dict.iteritems():
	if len(value["Neighbours"]) >= 5:
		while True:
			if len(relation_dict[key]["Neighbours"])==4:
				break
			max=0
			max_item=""
			for item in value["Neighbours"]:
				if len(relation_dict[item]["Neighbours"])>= max:
					max=len(relation_dict[item]["Neighbours"])
					max_item=item
			relation_dict[key]["Neighbours"].remove(max_item)
			relation_dict[max_item]["Neighbours"].remove(key)			

to_pop=[]
for key,value in relation_dict.iteritems():
	if len(value["Neighbours"])!=0:
		list_of_cities.add(key)
	else:
		to_pop.append(key)

for item in to_pop:
	relation_dict.pop(item,None)



relation_list=[]
flag=False

for key,value in relation_dict.iteritems():
	for item in value["Neighbours"]:
		for check in relation_list:
			if item in check and key in check:
				flag=True
		if flag==True:
			flag=False
			continue
		relation_list.append(key+","+item)


list_of_cities=sorted(list(list_of_cities))
print relation_list
print list_of_cities

graph = pydot.Dot(graph_type='graph')
for city in list_of_cities:
	pydot.Node(city, style="filled", fillcolor="red")

for item in relation_list:
	city_1=item.split(",")[0]
	city_2=item.split(",")[1]
	graph.add_edge(pydot.Edge(city_1,city_2))
	graph.write_png('/proj/SENSS/DHS/pic.png')
                        
