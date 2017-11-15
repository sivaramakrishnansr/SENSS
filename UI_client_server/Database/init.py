import MySQLdb

password=""
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()

try: 
	cur.execute("CREATE DATABASE SENSS")
	print "Database SENSS created"
except:
	print "Database SENSS already exists"

cur.execute("USE SENSS")

try:
	cur.execute("CREATE TABLE DIRECT_FLOODS(ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,REQUEST_TO VARCHAR(50),O_TIME VARCHAR(50),TOTAL_TIMES VARCHAR(50),TAG VARCHAR(50),DONE VARCHAR(1),RESULT VARCHAR(50000),FILTER VARCHAR(5000),PROXY VARCHAR(1),ATTACK VARCHAR(1),ATTACK_FROM VARCHAR(200))")
	print "Table DIRECT_FLOODS created"
except:
	print "Table DIRECT_FLOODS already exists"

try:
	cur.execute("CREATE TABLE CROSSFIRE(ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,REQUEST_TO VARCHAR(50),O_TIME VARCHAR(50),TOTAL_TIMES VARCHAR(50),TAG VARCHAR(50),DONE VARCHAR(1),RESULT VARCHAR(50000),FILTER VARCHAR(5000))")
	print "Table CROSSFIRE created"
except:
	print "Table CROSSFIRE already exists"


try:
	cur.execute("CREATE TABLE FILTERS(ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,DPID VARCHAR(50),MATCH_FLOW VARCHAR(50))")
	print "Table FILTERS created"
except:
	print "Table FILTERS already exists"

try:
	cur.execute("CREATE TABLE `CLIENT_LOGS` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `log_type` varchar(45) NOT NULL, `match_field` text, `packet_count` bigint(20) DEFAULT NULL, `byte_count` bigint(20) DEFAULT NULL, `speed` varchar(45) DEFAULT NULL, `flag` int(1) DEFAULT 0, `active` int(1) DEFAULT NULL, `frequency` int(11) DEFAULT 0, `end_time` int(15) DEFAULT 0, PRIMARY KEY (`id`))")
	print "Table CLIENT_LOGS created"
except Exception as e:
	print e
	print "Table CLIENT_LOGS already exists"

cur.close()
cur=db.cursor()

try: 
	cur.execute("CREATE DATABASE SENSS_CLIENT")
	print "Database SENSS_CLIENT created"
except:
	print "Database SENSS_CLIENT already exists"

cur.execute("USE SENSS_CLIENT")

try:
	cur.execute("CREATE TABLE `AS_URLS` (`id` int(11) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `server_url` varchar(255) NOT NULL, `links_to` text, `self` int(1) DEFAULT 0, PRIMARY KEY (`id`))")
	print "Table AS_URLS created"
except Exception as e:
	print e
	print "Table AS_URLS already exists"
	
try:
	cur.execute("CREATE TABLE `MONITORING_RULES` (`id` int(11) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `match_field` text, `frequency` int(5) DEFAULT 0, `end_time` int(15) DEFAULT 0, PRIMARY KEY (`id`))")
	print "Table MONITORING_RULES created"
except Exception as e:
	print e
	print "Table MONITORING_RULES already exists"
