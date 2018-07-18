#
# Copyright (C) 2018 University of Southern California.
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

import sys
import subprocess
from subprocess import call

fileName = sys.argv[1]

cmd = "mkdir ca"
print(cmd)
call(cmd, shell=True)

# Create root certificate
password = "password"
country = "US"
state = "CA"
locality = "LA"
organization = "STEEL"
organizationalunit = "SENSS"
email = "senss@isi.edu"
commonname = "steel1.isi.edu"
cmd = "openssl req -newkey rsa:4096 -sha256 -keyout ca/rootkey.pem -out ca/rootreq.pem -passin pass:" + password + " -passout pass:" + password
cmd += " -subj \"/C=" + country + "/ST=" + state + "/L=" + locality + "/O=" + organization + "/OU=" + organizationalunit + "/CN=" + commonname + "/emailAddress=" + email + "\""
print(cmd)
call(cmd, shell=True)

# Sign root certificate with it's own private key
cmd = "openssl x509 -req -in ca/rootreq.pem -sha256 -signkey ca/rootkey.pem -out ca/rootcert.pem -passin pass:" + password
print(cmd)
call(cmd, shell=True)

# Install CA certificate as trusted certificate
cmd = "mkdir /usr/share/ca-certificates/extra"
print(cmd)
call(cmd, shell=True)

cmd = "cp ca/rootcert.pem /usr/share/ca-certificates/extra/rootcert.crt"
print(cmd)
call(cmd, shell=True)

#cmd = "sudo dpkg-reconfigure ca-certificates"
#print(cmd)
#call(cmd, shell=True)

cmd = "update-ca-certificates"
print(cmd)
call(cmd, shell=True)

cmd = "mkdir clients"
print(cmd)
call(cmd, shell=True)
cmd = "mkdir certificates"
print(cmd)
call(cmd, shell=True)
# Read file and create client certificates
lines = [line.rstrip('\n') for line in open(fileName)]
for line in lines:
    node = line.split(":",2)[0]
    prefix = line.split(":", 2)[1]

    #commonname = node + ".isi.edu"
    commonname = node

    # Create one client certificate
    cmd = "openssl req -newkey rsa:4096 -sha256 -keyout clients/" + node + "key.pem -out clients/" + node + "req.pem -passin pass:" + password + " -passout pass:" + password
    cmd += " -subj \"/C=" + country + "/ST=" + state + "/L=" + locality + "/O=" + organization + "/OU=" + organizationalunit + "/CN=" + commonname + "/emailAddress=" + email + "\""
    print(cmd)
    call(cmd, shell=True)

    # Sign client certificate using root's private key
    nsComment = prefix
    # nsComment can only be given from an extention file.
    f = open('clients/extConf', 'w')
    f.write("[req]\ndistinguished_name=dn\n[ dn ]\n[ ext ]\nnsComment=\"" + nsComment + "\"")
    f.close()
    # Signing
    cmd = "openssl x509 -req -in clients/" + node + "req.pem -sha256 -CA ca/rootcert.pem -CAkey ca/rootkey.pem -CAcreateserial -out clients/" + node + "cert.pem -passin pass:" + password
    cmd += " -extfile clients/extConf -extensions ext"
    print(cmd)
    call(cmd, shell=True)

    cmd = "cp clients/" + node + "cert.pem" + " certificates/" + node + "cert.pem"
    print(cmd)
    call(cmd, shell=True)

cmd = "cp ca/rootcert.pem" + " certificates/rootcert.pem"
print(cmd)
call(cmd, shell=True)

# Verify certificates:
print("\n*****Verify certificates*****")
for line in lines:
    node = line.split(":",2)[0]
    cmd = "openssl verify -CAfile certificates/rootcert.pem certificates/" + node + "cert.pem"
    result = subprocess.check_output(cmd, shell=True).rstrip()
    if (result != "certificates/" + node + "cert.pem: OK"):
        print(node + " NOT verified: " + result)
    else:
        print(node + " verified: " + result)
