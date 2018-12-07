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
sudo service apache2 restart
