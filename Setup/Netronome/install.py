from start_trafgen import start_attack
from generate_ns import generate_ns
header="""# Copyright (C) 2017 University of Southern California.
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
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA."""

print header
print 
print "INSTALLATION"
print "[1] SENSS - Consists of a senss client and a senss server. SENSS client can send requests to the SENSS server to monitor and filter traffic"
print
print "[2] SENSS Proxy - Consists of a senss client, sensss server and a proxy. SENSS client can send requests to the SENSS server to monitor and filter traffic. If the senss client is overwhelmed with traffic, SENSS functionalities are deligated to the SENSS proxy"
print
print "[3] SENSS large scale testing with OVS - Large scale testing with cogent topology from topology zoo. Can be customised for different topologies."
print 
print "[4] SENSS large scale testing with Netronome OVS - Large scale testing with Netronome Smart NIC supporting OVS. Can generate upto 1Tbps of attack traffic."
print
print "[5] SENSS switch testing"
option = int(input("SENSS>"))
if option==4:
	print "[1] View README"
	print "[2] Generate NS file"
	print "[3] Setup experiment"
	print "[4] Start traffic"
	option = int(input("SENSS>"))
	if option ==1:
		print "Configure the nodes file before generating the NS file for the experiment. The nodes file consists of the set of nodes involved in this experiment. Various fields are described below.  "
		print "Deter node - Name of the deter node included in the experiment"
		print "Number of netronome ports - Number of ports which are connected to the switch" 
		print "Node type [client/server] - Can operate as a SENSS client or a SENSS server"
		print "AS name - AS name for the code. Reflects in the topology of GUI"
		print "Server URL - SENSS server URL"
		print "Links to - Peering AS"
		print "Rate of traffic - Percentage of 40Gbps traffic to be generated towards the SENSS client"
		print "Duration of traffic - duration of traffic to be generated"
		print 
		print "Use the installer to generate the NS file and and use the NS file to start the experiment on DETER"
	if option==2:
		generate_ns()
	if option==4:
		start_attack()
