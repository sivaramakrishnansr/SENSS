import MySQLdb

password="usc558l"
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()

try: 
	cur.execute("CREATE DATABASE SENSS")
	print "Database SENSS created"
except:
	print "Database SENSS already exists"

cur.execute("USE SENSS")

try:
	cur.execute("CREATE TABLE `CLIENT_LOGS` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `log_type` varchar(45) NOT NULL, `match_field` text, `packet_count` bigint(20) DEFAULT NULL, `byte_count` bigint(20) DEFAULT NULL, `speed` varchar(45) DEFAULT NULL, `flag` int(1) DEFAULT 0, `active` int(1) DEFAULT NULL, `frequency` int(11) DEFAULT 0, `end_time` int(15) DEFAULT 0,`threshold` int(15) DEFAULT 10, PRIMARY KEY (`id`))")
	print "Table CLIENT_LOGS created"
except Exception as e:
	print e
	print "Table CLIENT_LOGS already exists"
	cur.execute("DROP TABLE CLIENT_LOGS")
	cur.execute("CREATE TABLE `CLIENT_LOGS` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `log_type` varchar(45) NOT NULL, `match_field` text, `packet_count` bigint(20) DEFAULT NULL, `byte_count` bigint(20) DEFAULT NULL, `speed` varchar(45) DEFAULT NULL, `flag` int(1) DEFAULT 0, `active` int(1) DEFAULT NULL, `frequency` int(11) DEFAULT 0, `end_time` int(15) DEFAULT 0,`threshold` int(15) DEFAULT 10, PRIMARY KEY (`id`))")
	print "Table CLIENT_LOGS created"


try:
	cur.execute("CREATE TABLE `SERVER_LOGS` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `request_type` varchar(45) NOT NULL,`as_name` varchar(45) NOT NULL, `match_field` text, `packet_count` bigint(20) DEFAULT NULL, `end_time` int(15) DEFAULT 0,`byte_count` bigint(20) DEFAULT NULL,valid_request INT DEFAULT NULL,prefix_allowed varchar(45) DEFAULT NULL, speed varchar(25) DEFAULT NULL,PRIMARY KEY (`id`))")
	print "Table SERVER_LOGS created"
except Exception as e:
	print e
	print "Table SERVER_LOGS already exists"
	cur.execute("DROP TABLE SERVER_LOGS")
	cur.execute("CREATE TABLE `SERVER_LOGS` (`id` bigint(20) NOT NULL AUTO_INCREMENT, `request_type` varchar(45) NOT NULL,`as_name` varchar(45) NOT NULL, `match_field` text, `packet_count` bigint(20) DEFAULT NULL, `end_time` int(15) DEFAULT 0,`byte_count` bigint(20) DEFAULT NULL,valid_request INT DEFAULT NULL,prefix_allowed varchar(45) DEFAULT NULL, speed varchar(25) DEFAULT NULL,PRIMARY KEY (`id`))")
	print "Table SERVER_LOGS created"



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
	cur.execute("DROP TABLE AS_URLS")
	cur.execute("CREATE TABLE `AS_URLS` (`id` int(11) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `server_url` varchar(255) NOT NULL, `links_to` text, `self` int(1) DEFAULT 0, PRIMARY KEY (`id`))")
	print "Table AS_URLS created"
	
try:
	cur.execute("CREATE TABLE `MONITORING_RULES` (`id` int(11) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `match_field` text, `frequency` int(5) DEFAULT 0, `end_time` int(15) DEFAULT 0, `monitor_id` bigint(20) DEFAULT 0, PRIMARY KEY (`id`))")
	print "Table MONITORING_RULES created"
except Exception as e:
	print e
	print "Table MONITORING_RULES already exists"
	cur.execute("DROP TABLE MONITORING_RULES")
	cur.execute("CREATE TABLE `MONITORING_RULES` (`id` int(11) NOT NULL AUTO_INCREMENT, `as_name` varchar(45) NOT NULL, `match_field` text, `frequency` int(5) DEFAULT 0, `end_time` int(15) DEFAULT 0, `monitor_id` bigint(20) DEFAULT 0, PRIMARY KEY (`id`))")
	print "Table MONITORING_RULES created"
	
