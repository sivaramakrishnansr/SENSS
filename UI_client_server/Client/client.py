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
data=""
for item in results:
	data=data+json.dumps(item)+"\n"
s = socket.socket()             # Create a socket object
host = "56.0.0.1"     # Get local machine name
port = 60000                    # Reserve a port for your service.

s.connect((host, port))
data=[data[i:i+1024] for i in range(0, len(data), 1024)]
for i in data:
       print i
       s.send(i)

print('Done sending')
s.close()
