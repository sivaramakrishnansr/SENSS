echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
mkdir -p /mnt/huge
grep -q hugetlbfs /proc/mounts || mount -t hugetlbfs nodev /mnt/huge
# using one VF
/root/DPDK/dpdk_nic_bind.py -b nfp_uio 82:08.0
# using more VF
/root/DPDK/dpdk_nic_bind.py -b nfp_uio 82:08.1
#/root/DPDK/l2fwd -c 0x5 --socket-mem=1024,1024 -n 4 --log-level=7 -w 82:08.0 --file-prefix=dpdk0_ -- -p 0x1
# using more VF
/root/DPDK/l2fwd -c 0x55 --socket-mem=1024,1024 -n 4 --log-level=7 -w 82:08.0 82:08.1--file-prefix=dpdk0_ -- -p 0x3
