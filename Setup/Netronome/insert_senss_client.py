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
cmd="""INSERT INTO AS_URLS (as_name,server_url,links_to,self) VALUES ('%s','%s','%s','%d')"""%(as_name,server_url,links_to,self)
print cmd
cur.execute(cmd)
db.commit()
