import sys
import json

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
file_to_write=open("list_of_cities","w")

for city in list_of_cities:
        file_to_write.write(city+"-"+str(list_of_cities.index(city)+1)+"\n")
file_to_write.close()
