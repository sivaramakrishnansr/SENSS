
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
import urllib2
import sys

def process(dpid,controller_ip):

        port_list=[1,2]
        method = "DELETE"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/clear/"+str(dpid))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()


        data_to_send={'dpid': int(dpid),'priority':0,'match':{'in_port':port_list[0]},'actions':[{'type':'OUTPUT','port': port_list[1]}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()

        data_to_send={'dpid': int(dpid),'priority':0,'match':{'in_port':port_list[1]},'actions':[{'type':'OUTPUT','port': port_list[0]}]}
        method = "POST"
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        request = urllib2.Request("http://"+controller_ip+":8080/stats/flowentry/add", data=str(data_to_send))
        request.add_header("Content-Type",'application/json')
        request.get_method = lambda: method
        connection = opener.open(request)
        data = connection.read()
        print "Added Flows"


controller_ip=sys.argv[1]
method = "GET"
handler = urllib2.HTTPHandler()
opener = urllib2.build_opener(handler)
request = urllib2.Request("http://"+controller_ip+":8080/stats/switches")
request.get_method = lambda: method
connection = opener.open(request)
data = eval(connection.read())
print data
for dpid in data:
	process(dpid,controller_ip)
