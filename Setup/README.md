* Setting up the controller
    * Install RYU Dependencies and RYU
        * cd /users/satyaman/ryu_dependencies
        * sudo python ryu_install.py
        * cd /users/satyaman/ryu/ryu-master
        * sudo python setup.py instal
    * Install Controller Dependencies
        * cd /proj/SENSS/DHS/Setup
        * sudo sh controller_setup.sh
        * set password as usc558l
    * Transfer files to UCSB
        * cd /proj/SENSS/ucsb
        * sudo cp -rf html /var/www
    * Run Controller on Screen
        * cd /users/satyaman/ryu/ryu-master/ryu/app
        * sudo ryu-manager ofctl_rest.py
    * Setup database on controller
        * cd /proj/SENSS/ucsb/html/Database
        * sudo python init.py
        *
* Running Quagga Setup
    * cd /proj/SENSS/DHS/Setup
    * change the experiment name on quagga_start.py
    * python quagga_start.py
* Running openvswitch setup
    * cd /proj/SENSS/DHS/Setup
    * change the experiment name on openvswitch_start.py and change the controller IP
        * python openvswitch_start.py 
    




Notes
* Legit Sources of Traffic
    * From 30 to 60
        * sudo ./flooder --src 30.0.0.1 --srcmask 255.255.255.255 --dst 60.0.0.2 --dstmask 255.255.255.255 --highrate 100
    * From 33 to 60
        * sudo ./flooder --src 33.0.0.1 --srcmask 255.255.255.255 --dst 60.0.0.5 --dstmask 255.255.255.255 --highrate 100
    * From 19 to 60
        * sudo ./flooder --src 19.0.0.1 --srcmask 255.255.255.255 --dst 60.0.0.2 --dstmask 255.255.255.255 --highrate 100
* Malicious Sources
    * From 67 to 60
        * sudo ./flooder --src 67.0.0.1 --srcmask 255.255.255.255 --dst 60.0.0.19 dstmask 255.255.255.255 --highrate 1000
    * From 84 to 60
        * sudo ./flooder --src 84.0.0.1 --srcmask 255.255.255.255 --dst 60.0.0.9 dstmask 255.255.255.255 --highrate 1000
    * From 76 to 60
        * sudo ./flooder --src 76.0.0.1 --srcmask 255.255.255.255 --dst 60.0.0.7 --dstmask 255.255.255.255 --highrate 1000
* Setup
    * screen -R proxy_server
    * screen -R proxy_client
    * screen -R controller
    * screen -R attack , attack_2 , attack_3
