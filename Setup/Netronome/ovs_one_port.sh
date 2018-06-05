sudo ovs-vsctl --if-exist del-br br0
sudo ovs-vsctl add-br br0 -- set Bridge br0 "protocols=OpenFlow13"
sudo ovs-ofctl -O OpenFlow13 del-flows br0
sudo ovs-ofctl -O OpenFlow13 del-groups br0 group_id=0
sudo ovs-vsctl add-port br0 sdn_p0 -- set Interface sdn_p0 ofport_request=1
sudo ovs-vsctl add-port br0 sdn_v0.0 -- set Interface sdn_v0.0 ofport_request=2
sudo ovs-vsctl add-port br0 sdn_v0.1 -- set Interface sdn_v0.1 ofport_request=3
sudo ovs-vsctl add-port br0 sdn_v0.2 -- set Interface sdn_v0.2 ofport_request=4
#sudo ovs-vsctl set-controller br0 tcp:0.0.0.0:6633
ifconfig sdn_p0 up
ifconfig sdn_v0.0 up
ifconfig sdn_v0.1 up


