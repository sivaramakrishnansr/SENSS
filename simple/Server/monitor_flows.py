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

import re
from netaddr import IPAddress,IPNetwork
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
multiply=int(sys.argv[1])
legit_traffic=sys.argv[2]
#filter_1="ipv4,nw_src=39.0.0.1,nw_dst=57.0.0.1"
#filter_2="ipv4,nw_src=39.0.0.1,nw_dst=57.0.0.2"
#filter_1=sys.argv[2]
#filter_2=sys.argv[3]

last_time={}
while True:
	db.commit()
	cur.execute("SELECT * FROM CLIENT_LOGS")
	all_ids=set()
	completed_ids=set()
	for item in cur.fetchall():
		id=int(item[0])
		#if id!=1:
		#	continue
		all_ids.add(id)
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
		byte_counts={}
		for dump in output:
			derived_fields={}
			match_fields=re.split(',\s*(?![^()]*\))', dump)
			for match in match_fields[1:]:
				if "(" in match and ")" in match and "," in match:
					start_key=match.split("(")[0]	
					for item in match.split("(")[1].replace(")","").split(","):
						sub_key=item.split("=")[0]
						key=start_key+"_"+sub_key
						sub_value=item.split("=")[1]
						if key=="ipv4_src" or key=="ipv4_dst":
							if "/" in sub_value:
								ip_addr=sub_value.split("/")[0]
								subnet=IPAddress(sub_value.split("/")[1]).netmask_bits()
								sub_value=ip_addr+"/"+str(subnet)
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
			total=0
			found=0
			for key,value in match_field["match"].iteritems():
				total=total+1
				if key in derived_fields:
					if key=="ipv4_src" or key=="ipv4_dst":
						if IPNetwork(value) == IPNetwork(derived_fields[key]):
							found=found+1
						continue
					if value==derived_fields[key]:
						found=found+1
					
			if "ipv4_dst" in derived_fields:
				if IPNetwork(legit_traffic) in IPNetwork(derived_fields["ipv4_dst"]):
					if id not in byte_counts:
						byte_counts[id]=0
					byte_counts[id]=byte_counts[id]+int(derived_fields["bytes"])
					#print colored( "ADDING "+str(byte_counts[id])+" "+str(derived_fields[key]+" "+str(legit_traffic)),"red")
			current_time=time.time()
			if found==total:
				if id not in byte_counts:
					byte_counts[id]=0
				print colored("Byte Count "+str(byte_counts[id]),"yellow")
				new_byte_count=int(derived_fields["bytes"])
				if "actions" in derived_fields:
					if derived_fields["actions"]=="drop":
						print "HERE to DROP"
						new_byte_count=0
				#print "HERE",new_byte_count
				byte_counts[id]=byte_counts[id]+new_byte_count
		if id not in last_time:
			last_time[id]=time.time()
			continue
		total_time=current_time-last_time[id]
		if total_time<frequency:
			completed_ids.add(id)
			continue
		if id in byte_counts:	
			new_byte_count=byte_counts[id]
			speed=round(((new_byte_count-old_byte_count)*8)/float(total_time),2)
		else:
			speed=0
		last_time[id]=current_time
		if speed<0:
			speed=0
		speed=str(speed*multiply)
		cmd="""UPDATE CLIENT_LOGS SET byte_count='%d',speed='%s' WHERE id='%d'"""%(new_byte_count,speed,id)
		cur.execute(cmd)
		db.commit()
		print colored("Matching "+json.dumps(match_field["match"]),"green")
		print colored("Old Byte Count "+str(old_byte_count),"yellow"),colored("New Byte Count "+str(new_byte_count),"green")
		print derived_fields
		print colored("Speed "+str(speed),"red"),"\n"
		print colored("Total time "+str(total_time)+" Diff "+str(new_byte_count-old_byte_count),"red")
		print	
		completed_ids.add(id)
		#time.sleep(3)	
	remaining_ids=all_ids-completed_ids
	for id in remaining_ids:
		new_byte_count=0
		speed=0
		cmd="""UPDATE CLIENT_LOGS SET byte_count='%d',speed='%s' WHERE id='%d'"""%(new_byte_count,speed,id)
		cur.execute(cmd)
		db.commit()
