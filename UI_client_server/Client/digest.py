import json
import requests
import time
import urllib2
import MySQLdb
import os

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()

if True:
	os.system("/var/www/html/SENSS/AMON-SENSS-NEW/AMON-SENSS/as -r /var/cache/nfdump4 -v")
	#4 1546411203 START 2804 940 20 src ip 52.0.0.1 and dst ip 50.0.0.1 and proto udp
	try:
	        f=open("/var/www/html/SENSS/AMON-SENSS-NEW/AMON-SENSS/alerts.txt","r")
        	for line in f:
                	src_ip=line.strip().split(" ")[8]	
			dst_ip=line.strip().split(" ")[12]
        	        break	
	        f.close()
		print (src_ip,dst_ip)
	except:
		print ("Not ready")
	exit(1)
        if src_ip!="":
		input={}
		as_name="hpc052"
		input["as_name"]=[as_name]
		input["monitor_frequency"]=1
		input["monitor_duration"]=1000
		input["monitor_type"]="user"
		input["match"]={"ipv4_src":src_ip,"ipv4_dst":dst_ip,"eth_type": 2048}
		cur.execute("USE SENSS_CLIENT")
		sql=("INSERT INTO AMON_SENSS (as_name, match_field, frequency, monitor_duration, type) VALUES ('%s','%s',%d,%d,'%s')") % (as_name,json.dumps(input["match"]), input["monitor_frequency"], input["monitor_duration"],"DAMN")
		cur.execute(sql)
		db.commit()
		
