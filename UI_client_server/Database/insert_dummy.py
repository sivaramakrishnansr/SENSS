import MySQLdb
import json

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()


cur.execute("USE SENSS")
cur.execute("DELETE FROM CLIENT_LOGS")
as_name=50
match_field={"dpid": 91487349078,"priority": 11111,"match":{"in_port":3,"nw_src": "192.168.0.1","eth_type": 2048},"actions":[{"type":"OUTPUT","port": 2}]}

match_field=json.dumps(match_field)
log_type="monitoring"
frequency=50
#"UPDATE DIRECT_FLOODS SET RESULT='"+result+"'
cmd="""INSERT INTO CLIENT_LOGS (id,as_name,log_type,match_field,packet_count,byte_count,speed,flag,active,frequency,end_time) VALUES (NULL,'%s','%s','%s','%d','%d','%s','%d','%d','%d','%d')"""%(as_name,log_type,match_field,0,0,'0Mbps',0,0,1,0)
#(as_name,match_field,log_type,frequency)
print cmd
cur.execute(cmd)
db.commit()
