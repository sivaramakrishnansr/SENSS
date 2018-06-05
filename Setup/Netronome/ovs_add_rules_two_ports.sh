#This is for getting the BGP updates
#sudo ovs-vsctl add-port br0 sdn_p0 -- set Interface sdn_p0 ofport_request=1
#sudo ovs-vsctl add-port br0 sdn_p1 -- set Interface sdn_p1 ofport_request=2
#sudo ovs-vsctl add-port br0 sdn_v0.0 -- set Interface sdn_v0.0 ofport_request=3
#sudo ovs-vsctl add-port br0 sdn_v0.1 -- set Interface sdn_v0.1 ofport_request=4

#BGP traffic
curl -X POST -d '{"dpid": 91487349002,"priority": 1,"match":{"in_port":1},"actions":[{"type":"OUTPUT","port": 3}]}' http://localhost:8080/stats/flowentry/add
curl -X POST -d '{"dpid": 91487349002,"priority": 1,"match":{"in_port":3},"actions":[{"type":"OUTPUT","port": 1}]}' http://localhost:8080/stats/flowentry/add

#Traffic generator 
curl -X POST -d '{"dpid": 91487349002,"priority": 1,"match":{"in_port":4},"actions":[{"type":"OUTPUT","port": 1},{"type":"OUTPUT","port":2}]}' http://localhost:8080/stats/flowentry/add

