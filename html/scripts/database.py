
#
# Copyright (C) 2016 University of Southern California.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import MySQLdb
import sys

password=""
host="root"
db=MySQLdb.connect(host="localhost",port=3306,user=host,passwd=password)
cur=db.cursor()

def init_database():
	try: 
		cur.execute("CREATE DATABASE SENSS")
		print "Database SENSS created"
	except:
		print "Database SENSS already exists"

	cur.execute("USE SENSS")
	try:
		cur.execute("CREATE TABLE SENSS_LOGS(ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,REQUEST_TYPE VARCHAR(20),REQUEST_FROM VARCHAR(20),REQUEST_TO VARCHAR(20),OUTPUT VARCHAR(1000),DURATION VARCHAR(20),TIME VARCHAR(200))")
		print "Table SENSS_LOGS created"
	except:
		print "Table SENSS_LOGS already exists"
	try:
		cur.execute("CREATE TABLE SENSS_CUSTOMERS(ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,CUSTOMER_NAME VARCHAR(20),IP VARCHAR(2000),PUBLIC_KEY VARCHAR(200),RPKI VARCHAR(1))")
		print "Table SENSS_CUSTOMERS created"
	except:
		print "Table SENSS_CUSTOMERS already exists"




init_database()
