import MySQLdb
import json
import sys

password=sys.argv[1]
as_name=sys.argv[2]
server_url=sys.argv[3]
links_to=sys.argv[4]
self=int(sys.argv[5])
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()
cur.execute("USE SENSS_CLIENT")
#server_url=as_name.replace("hpc0","")+".0.0.1"
cmd="""INSERT INTO AS_URLS (as_name,server_url,links_to,self) VALUES ('%s','%s','%s','%d')"""%(as_name,server_url,links_to,self)
print cmd
cur.execute(cmd)
db.commit()
