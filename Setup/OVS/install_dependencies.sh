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

sudo apt-get update
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password usc558l'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password usc558l'
sudo apt-get install mysql-server --assume-yes
sudo apt-get install apache2 --assume-yes
sudo apt-get install php5 --assume-yes
sudo apt-get install python-mysqldb --assume-yes
sudo apt-get install php5-curl --assume-yes
sudo apt-get install quagga --assume-yes
sudo apt-get install python-pip --assume-yes
sudo apt-get install python-greenlet --assume-yes
sudo apt-get install msgpack-python --assume-yes
sudo apt-get install python-routes --assume-yes
sudo apt-get install python-webob --assume-yes
sudo apt-get install python paramiko --assume-yes
sudo apt-get install php5-mysql --assume-yes
sudo apt-get install php5-mysqlnd --assume-yes
sudo apt-get install python-pexpect --assume-yes
sudo apt-get install python-dateutil --assume-yes
sudo apt-get install python-termcolor --assume-yes
sudo apt-get install nload --assume-yes
sudo pip install /users/satyaman/ryu_dependencies/eventlet-0.15.2-py2.py3-none-any.whl
sudo pip install /users/satyaman/ryu_dependencies/six-1.9.0-py2.py3-none-any.whl
sudo dpkg -i /users/satyaman/ryu_dependencies/python-pbr_0.8.2-0ubuntu1_all.deb
sudo pip install /users/satyaman/ryu_dependencies/netaddr-0.7.18-py2.py3-none-any.whl
sudo pip install /users/satyaman/ryu_dependencies/stevedore-1.1.0-py2.py3-none-any.whl
sudo pip install /users/satyaman/ryu_dependencies/oslo.config-1.7.0-py2.py3-none-any.whl