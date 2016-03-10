
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
import json
import sys
import pydot

ip_dict={}
file_to_read=open("/var/www/html/data/quagga_input","r")
city_list=set()
for line in file_to_read:
        line=line.strip().split("qwerty123")
        ip=line[0]
        value=json.loads(line[1])
        ip_dict[ip]=value

for key,value in ip_dict.iteritems():
	city_list.add(key)

city_list=sorted(list(city_list))
city=sys.argv[1]

print ip_dict[city]
graph = pydot.Dot(graph_type='digraph')

node_dict={}
node_dict[city]=pydot.Node(city, style="filled", fillcolor="red")
graph.add_node(node_dict[city])

for item in ip_dict[city]:
	for ip,asn in item.iteritems():
		neighbor_city=city_list[int(asn)-1]
		print city,neighbor_city
		node_dict[neighbor_city]=pydot.Node(neighbor_city, style="filled", fillcolor="red")
		graph.add_node(node_dict[neighbor_city])
		graph.add_edge(pydot.Edge(node_dict[neighbor_city],node_dict[city],label="THIS",color="blue"))

graph.write_png('/var/www/html/example2_graph.png')

