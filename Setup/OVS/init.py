#
# Copyright (C) 2018 University of Southern California.
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

