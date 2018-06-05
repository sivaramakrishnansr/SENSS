import MySQLdb
import sys

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()

cur.execute("USE SENSS_CLIENT")
#cur.execute("DELETE FROM AS_URLS")

node=sys.argv[1]
links_to=sys.argv[2]
self=sys.argv[3]

server_address=node
#server_address=node.replace("hpc0","")+".0.0.1"
cur.execute("INSERT INTO AS_URLS (as_name,server_url,links_to,self) VALUES ('"+node+"','http://"+server_address+"/SENSS/UI_client_server/Server/api.php','"+node+"',"+self+")")
#cur.execute("INSERT INTO AS_URLS (as_name,server_url,links_to,self) VALUES ('hpc057','http://hpc057/SENSS/UI_client_server/Server/api.php','hpc039,hpc041,hpc042,hpc043,hpc044,hpc045,hpc046,hpc047,hpc048,hpc049,hpc050,hpc051,hpc052,hpc053,hpc054,hpc055,hpc056',1)")
#cur.execute("INSERT INTO AS_URLS (as_name,server_url,links_to,self) VALUES ('hpc054','http://hpc054/SENSS/UI_client_server/Server/api.php','hpc054',0)")
db.commit()
