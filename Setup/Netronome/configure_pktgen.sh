#sudo sed 's/link.link_speed = ETH_SPEED_NUM_NONE/link.link_speed = ETH_SPEED_NUM_40G/g' -i /opt/netronome/srcpkg/dpdk-ns/drivers/net/nfp/nfp_net.c
#cd /opt/netronome/srcpkg/dpdk-ns/ 
#sudo make
#sudo cp /proj/SENSS/SENSS_git/SENSS/Setup/Netronome/pktgen-3.4.5.zip /opt
#cd /opt/
#sudo rm -rf /opt/pktgen-3.4.5
#cd /opt/
#sudo unzip /opt/pktgen-3.4.5.zip
#cd /opt/pktgen-3.4.5
#sudo make clean RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc
sudo cp /proj/SENSS/lua-5.3.4.tar.gz /opt/pktgen-3.4.5/lib/lua/
cd /opt/pktgen-3.4.5/lib/lua 
#sudo make RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc
#sudo mkdir -p /opt/pktgen-3.4.5/lib/lua/src/lib/lua/src/x86_64-native-linuxapp-gcc/lib/
#sudo cp /opt/pktgen-3.4.5/lib/lua/lua-5.3.4/src/src/x86_64-native-linuxapp-gcc/lib/librte_lua.a /opt/pktgen-3.4.5/lib/lua/src/lib/lua/src/x86_64-native-linuxapp-gcc/lib/
#cd /opt/pktgen-3.4.5
#sudo make RTE_SDK=/opt/netronome/srcpkg/dpdk-ns RTE_TARGET=x86_64-native-linuxapp-gcc
