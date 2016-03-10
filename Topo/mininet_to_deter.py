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

def generate_ns_file(list_of_cities,relation_list):
	file_to_write=open("deter.ns","w")
	file_to_write.write("set ns [new Simulator]\n")
	file_to_write.write("source tb_compat.tcl\n\n")	

	#For every city there is one node
	for item in list_of_cities:
		city_number=list_of_cities.index(item)+1
		file_to_write.write("set i"+str(city_number)+" [$ns node]\n")
		file_to_write.write("tb-add-node-attribute $i"+str(city_number)+" containers:node_type qemu\n")
		file_to_write.write("tb-set-node-os $i"+str(city_number)+" Ubuntu1404-64-STD\n")

	file_to_write.write("\n")
	ip_dict={}
	link_counter=1
	for item in relation_list:

		if list_of_cities.index(item.split(",")[0])+1 > list_of_cities.index(item.split(",")[1])+1:
			item=item.split(",")
			relation_2=item[0]
			relation_1=item[1]
		else:
			item=item.split(",")
			relation_1=item[0]
			relation_2=item[1]
			

		ip_relation_1="10."+str(list_of_cities.index(relation_1)+1)+"."+str(list_of_cities.index(relation_2)+1)+".1"
		ip_relation_2="10."+str(list_of_cities.index(relation_1)+1)+"."+str(list_of_cities.index(relation_2)+1)+".2"
		ip_relation_3="10."+str(list_of_cities.index(relation_1)+1)+"."+str(list_of_cities.index(relation_2)+1)+".3"
		ip_relation_4="10."+str(list_of_cities.index(relation_1)+1)+"."+str(list_of_cities.index(relation_2)+1)+".4"

		file_to_write.write("set i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" [$ns node]\n")
		file_to_write.write("tb-add-node-attribute $i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" containers:node_type qemu\n")
		file_to_write.write("tb-set-node-os $i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" Ubuntu1404-64-STD\n")
		

		file_to_write.write("set link"+str(link_counter)+" [$ns duplex-link $i"+str(list_of_cities.index(relation_1)+1)+" $i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" 100Mb 0ms DropTail]\n")
		file_to_write.write("tb-set-ip-link $i"+str(list_of_cities.index(relation_1)+1)+" $link"+str(link_counter)+" "+ip_relation_1+"\n")
		file_to_write.write("tb-set-ip-link $i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" $link"+str(link_counter)+" "+ip_relation_2+"\n\n")
		link_counter=link_counter+1

		file_to_write.write("set link"+str(link_counter)+" [$ns duplex-link $i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" $i"+str(list_of_cities.index(relation_2)+1)+" 100Mb 0ms DropTail]\n")
		file_to_write.write("tb-set-ip-link $i"+str(list_of_cities.index(relation_1)+1)+"a"+str(list_of_cities.index(relation_2)+1)+" $link"+str(link_counter)+" "+ip_relation_3+"\n")
		file_to_write.write("tb-set-ip-link $i"+str(list_of_cities.index(relation_2)+1)+" $link"+str(link_counter)+" "+ip_relation_4+"\n\n")
		link_counter=link_counter+1




		neighbor_relation_1={ip_relation_4:str(list_of_cities.index(relation_2)+1)}
		neighbor_relation_2={ip_relation_1:str(list_of_cities.index(relation_1)+1)}

		#I Write IP DICT
		if relation_1 not in ip_dict:
			ip_dict[relation_1]=[]
		ip_dict[relation_1].append(neighbor_relation_1)
		if relation_2 not in ip_dict:
			ip_dict[relation_2]=[]
		ip_dict[relation_2].append(neighbor_relation_2)



	file_to_write.write("set controller [$ns node]\n")
	file_to_write.write("tb-set-node-os $controller Ubuntu1404-64-STD\n")
	file_to_write.write("tb-add-node-attribute $controller containers:node_type embedded_pnode\n")
	file_to_write.write("tb-set-hardware $controller MicroCloud\n\n")


	file_to_write.write("$ns rtproto Manual\n")
	file_to_write.write("$ns run\n")

	file_to_write.close()
	print

	file_to_write=open("/proj/SENSS/DHS/Setup/quagga_input","w")
	for key,value in ip_dict.iteritems():
        	file_to_write.write(str(key)+"qwerty123"+json.dumps(value)+"\n")
	file_to_write.close()
	print
	print
	for key,value in ip_dict.iteritems():
		print key,value

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
print relation_dict
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
					print max_item,max
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
print relation_dict
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
generate_ns_file(list_of_cities,relation_list)
