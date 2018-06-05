#echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
#mkdir -p /mnt/huge
#grep -q hugetlbfs /proc/mounts || mount -t hugetlbfs nodev /mnt/huge

#/root/DPDK/dpdk_nic_bind.py -b igb_uio 08:08.6

#PKTSIZE=${PKTSIZE:-1400}
echo "/root/DPDK/trafgen -c 0x5 --socket-mem=1024,1024 -n 4 --log-level=7 -w 08:08.6 --file-prefix=dpdk0_ -- -p 0x1 -T 5 --benchmark --packet-size ${PKTSIZE} --dst-ip 20.30.40.50 --dst-mac 00:01:02:03:83:05 --vary-dst mac,ip --flows-per-stream 1000 --bursts-per-stream 10 --streams 8"
