#!/bin/bash
apt-get install bind9 bind9utils bind9-doc
printf "options {\n\tdirectory \"/var/cache/bind\";\n\tlisten-on port 53 { localhost; any; };\n\tallow-query { localhost; any; };\n\tdnssec-validation auto;\n\tauth-nxdomain no;\n\tlisten-on-v6 { any; };\n};" > /etc/bind/named.conf.options
readarray dns < dns_entries.txt
for ((i=0; i<${#dns[@]}; i++))
do
	domain=$(echo "${dns[i]}" | cut -d' ' -f1)
	ip=$(echo "${dns[i]}" | cut -d' ' -f2)
	printf "\n\nzone \"${domain}\" {\n\ttype master;\n\tfile \"${domain}.zone\";\n};" >> /etc/bind/named.conf.default-zones
	printf "\$TTL 86400\n\n@ IN SOA att.net root.att.net (\n\t2016043008\n\t3600\n\t900\n\t604800\n\t86400\n\t)\n\n@\tIN\tNS\tsenss\nsenss\tIN\tA\t${ip}\n" > /var/cache/bind/${domain}.zone
done
named-checkconf
for ((i=0; i<${#dns[@]}; i++))
do
	domain=$(echo "${dns[i]}" | cut -d' ' -f1)
	ip=$(echo "${dns[i]}" | cut -d' ' -f2)
	named-checkzone ${domain} /var/cache/bind/${domain}.zone
done
systemctl enable bind9
systemctl start bind9
