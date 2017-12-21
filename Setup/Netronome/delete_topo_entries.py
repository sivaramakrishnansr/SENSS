import MySQLdb
import json
import sys

password=sys.argv[1]
db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd=password)
cur=db.cursor()
cur.execute("USE SENSS_CLIENT")
cur.execute("DELETE FROM AS_URLS")
db.commit()
