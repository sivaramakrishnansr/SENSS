#!/usr/bin/env python
import socket                   # Import socket module
import time
import MySQLdb
import json

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()

cur.execute("USE SENSS_CLIENT")
cur.execute("SELECT * FROM MONITORING_RULES")
results = cur.fetchall()
all_results=[]
fw=open("proxy_message","w")
for item in results:
	print item
	fw.write(json.dumps(item)+"\n")
fw.close()
s = socket.socket()             # Create a socket object
host = "56.0.0.1"     # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))

filename='proxy_message'
f = open(filename,'rb')
l = f.read(1024)
time.sleep(1)
while (l):
       s.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
f.close()

print('Done sending')
s.close()
