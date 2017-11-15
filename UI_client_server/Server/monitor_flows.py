import MySQLdb
import os
import json
import urllib2
import time
from dateutil import parser
import subprocess
from termcolor import colored

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()
cur.execute("USE SENSS")
while True:
	db.commit()
	cur.execute("SELECT * FROM CLIENT_LOGS")
	for item in cur.fetchall():
		id=int(item[0])
		as_name=str(item[1])
		log_type=str(item[2])
		match_field=json.loads(item[3])
		old_packet_count=int(item[4])
		old_byte_count=int(item[5])
		speed=item[6]
		flag=int(item[7])
		active=int(item[8])
		frequency=int(item[9])
		#end_time=parser.parse(item[10])
		priority=match_field["priority"]
		match_string="ipv4"
		for key,value in match_field["match"].iteritems():
			if key=="eth_type":
				continue
			match_string=match_string+","+key+"="+str(value)
		output = subprocess.check_output("ovs-dpctl dump-flows filter="+match_string, shell=True).strip().split(",")
		for item in output:
			if "packets" in item:
				new_packet_count=int(item.strip().split(":")[-1])
			if "bytes" in item:
				new_byte_count=int(item.strip().split(":")[-1])
		print colored("Old Byte Count "+str(old_byte_count),"yellow"),colored("New Byte Count "+str(new_byte_count),"green")
		print colored("Speed "+str(speed),"red"),"\n"
		speed=str((new_byte_count-old_byte_count)/float(frequency))+" bps"
		cmd="""UPDATE CLIENT_LOGS SET byte_count='%d',packet_count='%d',speed='%s' WHERE id='%d'"""%(new_byte_count,new_packet_count,speed,id)
		cur.execute(cmd)
		time.sleep(frequency)
