#!/bin/bash
ns=$1
sed -i "1s;^;nameserver ${ns} \n;" /etc/resolv.conf
