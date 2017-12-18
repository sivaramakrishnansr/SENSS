import os
print "sudo debconf-set-selections <<< \'mysql-server mysql-server/root_password password usc558l\'"
os.system("sudo debconf-set-selections <<< \'mysql-server mysql-server/root_password password usc558l\'")
exit(1)
os.system('sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password usc558l"')
os.system("sudo apt-get --assume-yes install mysql-server")
exit(1)
os.system('sudo apt-get update')
os.system('sudo apt-get install --assume-yes python-pip')
os.system('sudo apt-get install --assume-yes python-greenlet')
os.system('sudo apt-get install --assume-yes msgpack-python')
os.system('sudo apt-get install --assume-yes python-routes')
os.system('sudo apt-get install --assume-yes python-webob')
os.system('sudo apt-get install --assume-yes python paramiko')
os.system('sudo apt-get install --assume-yes quagga')

os.system('sudo pip install /users/satyaman/ryu_dependencies/eventlet-0.15.2-py2.py3-none-any.whl')
os.system('sudo pip install /users/satyaman/ryu_dependencies/six-1.9.0-py2.py3-none-any.whl')
os.system('sudo dpkg -i /users/satyaman/ryu_dependencies/python-pbr_0.8.2-0ubuntu1_all.deb')
os.system('sudo pip install /users/satyaman/ryu_dependencies/netaddr-0.7.18-py2.py3-none-any.whl')
os.system('sudo pip install /users/satyaman/ryu_dependencies/stevedore-1.1.0-py2.py3-none-any.whl')
os.system('sudo pip install /users/satyaman/ryu_dependencies/oslo.config-1.7.0-py2.py3-none-any.whl')

