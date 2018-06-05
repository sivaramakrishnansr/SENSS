import urllib2
import MySQLdb
import json

#Add threshold to website

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()

cur.execute("USE SENSS_CLIENT")
cur.execute("SELECT * FROM MONITORING_RULES")
results = cur.fetchall()
packet_count={}
while True:
	current_traffic={}
	all_traffic=[]
	all_as=[]
	for item in results:
		as_name=item[1]
		all_as.append(as_name)
		monitor_id=str(item[5])
		print as_name,monitor_id
		command="SELECT server_url FROM AS_URLS WHERE as_name='"+as_name+"'"
		cur.execute(command)
		server_url=str(cur.fetchall()[0][0])
		response = urllib2.urlopen(server_url+'?action=get_monitor&monitor_id='+monitor_id)
		packet_count = json.loads(response.read())["data"]["packet_count"]
		current_traffic[as_name]=packet_count
		all_traffic.append(packet_count)
		print
	for as in all_as:
		current_traffic[as]=current_traffic[as]/float(sum(all_traffic))*100
	break
