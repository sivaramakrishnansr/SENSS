import re
import MySQLdb
import os
import json
import urllib2
import time
from dateutil import parser
import subprocess
from termcolor import colored
import sys

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()
cur.execute("USE SENSS")
local_packet_count=0
#multiply=int(sys.argv[1])
#filter_1="ipv4,nw_src=39.0.0.1,nw_dst=57.0.0.1"
#filter_2="ipv4,nw_src=39.0.0.1,nw_dst=57.0.0.2"
#filter_1=sys.argv[2]
#filter_2=sys.argv[3]

while True:
	db.commit()
	cur.execute("SELECT * FROM CLIENT_LOGS")
	for item in cur.fetchall():
		id=int(item[0])
		if item[1]!=None:
			as_name=str(item[1])
		if item[2]!=None:		
			log_type=str(item[2])
		if item[3]!=None:
			match_field=json.loads(item[3])
		if item[4]!=None:
			old_packet_count=int(item[4])
		old_byte_count=0
		if item[5]!=None:
			old_byte_count=int(item[5])
		speed=0
		if item[6]!=None:
			speed=item[6]
		if item[7]!=None:
			flag=int(item[7])
		active=int(item[8])
		frequency=int(item[9])
		if active==0:
			continue
		#end_time=parser.parse(item[10])
		priority=match_field["priority"]
		match_string="ipv4"
		for key,value in match_field["match"].iteritems():
			if key=="eth_type":
				continue
			if key=="in_port":
				value=3
				continue
			match_string=match_string+","+key+"="+str(value)

		output = subprocess.check_output("ovs-dpctl dump-flows", shell=True).strip().split("\n")
		print output

		#split(',\s*(?![^{}]*\})', data)
		#['recirc_id(0),in_port(2),eth(src=7c:fe:90:f3:a1:42,dst=01:80:c2:00:00:0e),eth_type(0x88cc), packets:0, bytes:0, used:6.372s, actions:3'
		#, 'recirc_id(0),in_port(2),eth(src=7c:fe:90:f3:a1:41,dst=36:cb:b8:87:53:30),eth_type(0x0800),ipv4(src=0.0.0.0/128.0.0.0,dst=48.0.0.0/248.0.0.0,frag=no), 
		#packets:83, bytes:47941, used:0.772s, actions:3', 'recirc_id(0),in_port(4),eth(src=fa:07:ad:ad:84:fc,dst=7c:fe:90:f3:a1:41),eth_type(0x0800),
		#ipv4(src=0.0.0.0/128.0.0.0,dst=57.0.0.1,proto=17,frag=no), packets:13560192, bytes:20286047232, used:0.020s, actions:2,3']
		print
		for dump in output:
			derived_fields={}
			match_fields=re.split(',\s*(?![^()]*\))', dump)
			for match in match_fields[1:]:
				print match
				if "(" in match and ")" in match and "," in match:
					start_key=match.split("(")[0]	
					for item in match.split("(")[1].replace(")","").split(","):
						sub_key=item.split("=")[0]
						key=start_key+"_"+sub_key
						sub_value=item.split("=")[1]
						derived_fields[key]=sub_value
					continue
				if "(" in match and ")" in match and "," not in match:
					key=match.split("(")[0]
					item=match.split("(")[1].replace(")","")
					if key=="eth_type":
						item=int(item, 0)
					derived_fields[key]=item
					continue
				if ":" in match and "(" not in match and ")" not in match:
					key=match.split(":")[0]
					item=match.split(":")[1]
					derived_fields[key]=item
			print derived_fields
			print match_field["match"]
			print
		time.sleep(frequency)
		exit(1)
		continue
		#output = subprocess.check_output("ovs-dpctl dump-flows filter="+match_string, shell=True).strip().split(",")
		#print "ovs-dpctl dump-flows filter="+match_string
		
		output = subprocess.check_output("ovs-dpctl dump-flows filter="+filter_1, shell=True).strip().split(",")
		print "ovs-dpctl dump-flows filter="+filter_1
		new_packet_count=0
		new_byte_count=0
		for item in output:
			if "actions:drop" in item:
				new_packet_count=0
				new_byte_count=0
				continue
			if "packets" in item:
				new_packet_count=new_packet_count+int(item.strip().split(":")[-1])
			if "bytes" in item:
				new_byte_count=new_byte_count+int(item.strip().split(":")[-1])

		output = subprocess.check_output("ovs-dpctl dump-flows filter="+filter_2, shell=True).strip().split(",")
		print "ovs-dpctl dump-flows filter="+filter_2
		for item in output:
			if "actions:drop" in item:
				new_packet_count=0
				new_byte_count=0
				continue
			if "packets" in item:
				new_packet_count=new_packet_count+int(item.strip().split(":")[-1])
			if "bytes" in item:
				new_byte_count=new_byte_count+int(item.strip().split(":")[-1])



		update_packet_count=new_packet_count-local_packet_count
		local_packet_count=new_packet_count
		print colored("Old Byte Count "+str(old_byte_count),"yellow"),colored("New Byte Count "+str(new_byte_count),"green")
		print colored("Speed "+str(speed),"red"),"\n"
		speed=round(((new_byte_count-old_byte_count)*8)/float(frequency),2)
		if speed<0:
			speed=0
		speed=str(speed*multiply)
		if update_packet_count<0:
			update_packet_count=0
		update_packet_count=update_packet_count*multiply
		#cmd="""UPDATE CLIENT_LOGS SET byte_count='%d',packet_count='%d',speed='%s' WHERE id='%d'"""%(new_byte_count,new_packet_count,speed,id)
		cmd="""UPDATE CLIENT_LOGS SET byte_count='%d',packet_count='%d',speed='%s' WHERE id='%d'"""%(new_byte_count,update_packet_count,speed,id)
		cur.execute(cmd)
