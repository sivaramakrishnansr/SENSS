<h1>Setup</h1>

**1) graph_to_mininet.py**

Script is used to convert GraphML file into a mininet topology file. Topology Zoo provides several topologies in the GrpahML form. You can find the different topologies [here](http://www.topology-zoo.org/dataset.html).

`python graph_to_mininet.py -f path_to_graphml_file`

**2) mininet_to_deter.py**

Script is used to convert the mininet file obtained in the previous version to NS file. Deterlab accepts this NS file. This also creates a file named quagga_input which should be copied to the /proj/ folder in DETER. 

**3) list_of_cities**

A file generated in the Setup foldler which maps individual ASN to an unique number.
To access ASN Albama, look up for the number allocated in list_of_cities. For example, if Alabama is allocated 2,you could access Alabama,by

`ssh i2.experiment_name.project_name`

Note:
Each link between ASNs contains an OpenVSwitch which is used for the traffic_query and traffic_filter commands. To access this OpenVSwitch,

`ssh i{city_1_number}a{city_2_number}.experiment_name.project_name`

where city_1_number < city_2_number (These numbers are accesed using the list_of_cities file)

**4) Topo/generate_cities_relation.py**

Maps city from Topology to city_id . Used for reference

**4)connectivity_check.py**

This script is used to check if all the nodes which are setup in the experiment are available. Deterlab takes a few minutes to set up containerised experiments.


**5) Setting up the controller**

Install the dependencies for controller

`sudo python ryu_dependnties/install.py`

Install RYU

`cd ryu/ryu`<br />
`sudo python setup.py install`

Run controller

`cd ryu/ryu/app/`<br/>
`sudo ryu-manager ofctl_rest.py --ofp-list-host {ip_of_controller}`

Install Apache
`sudo apt-get install apache2 php5`
`sudo cp -r apache_files/* /var/www/html`

**5)setup.py**

Script is used to install OpenvSwitch and Quagga on nodes. Make sure that the controller is running. You could access the controller,
ssh controller.experiment_name.project_name

`python setup.py controller_ip`


<h1>SENSS</h1>

<h2>SENSS Server</h2>

`ssh user_name@users.deterlab.net -L 8118:controller.experiment_name.project_name.isi.deterlab.net:80`

To access the Server GUI:-
`http://localhost:8118/index.php`

<h3>Login</h3> 

A two factor authentication is used to validate the ISP.

![] (https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/SENSS.-.Login.png)

<h3>Add Switch</h3>

Add a new switch to the existing topology.
 
Name of the switch - Used for logging. In the case of a switch between Alabama(unique_number is 2) and Los Angeles(unique_number is 5) , the name of the switch is i2a5

Switch Username - Username of the node in deterlab running the switch

Switch Password - Password of the node in deterlab running the switch

Controller IP - IP address in which the controller is running

Controller Port - Port at which the controller is running

![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/SENSS.-.Add.Switch.png)

<h3>Remove Switch</h3>

Removes the switch from the topology by disconnecting the switch from the controller and uninstalling Openvswitch. 

Name of the switch - Used for logging. In the case of a switch between Alabama(unique_number is 2) and Los Angeles(unique_number is 5) , the name of the switch is i2a5

Switch Username - Username of the node in deterlab running the switch

Switch Password - Password of the node in deterlab running the switch

![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/SENSS.-.Remove.Switch.png)

<h3>Logs</h3>

Logs the requests/response from the customer.

![] (https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/Screen.Shot.2016-03-07.at.2.55.15.PM.png)

<h3>Add Customer</h3>

Enables the ISP to add a new customer
Customer Name - Name of the customer
IP Prefix - IP prefixes which are owned by the customers
Public Key/RPKI - Method adopted to verify the ownership of the IP prefixes.

![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/SENSS.-.Add.Customer.png)

<h3>View Customer</h3>

Views all the customers

![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/SENSS.-.View.Customer.png)



<h3>Client GUI</h3>

Can be accessed at `http://localhost:8118/direct_floods_form.php`

Client GUI can be used to handle direct floods without signature attacks. These are attacks which do not have any signature associated with them, and can be handled by SENSS constantly monitoring its traffic, and blocking traffic when a certain anamoly is detected.

<h3>Traffic Query</h3>

Sending traffic query request to the SENSS server.

Observation Time - Duration to observe the traffic

Total Request - Total number of requests

Tag - IN/OUT/SELF 

ISP - Choose the partnering ISP

![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/Screen.Shot.2016-03-07.at.3.03.49.PM.png)

<h3>View Logs</h3>
![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/Screen.Shot.2016-03-07.at.2.55.15.PM.png)

<h3>Client Program</h3>

<h4>Direct Floods</h4>
![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/Screen.Shot.2016-03-07.at.3.04.15.PM.png)

<h4>Crossfire Attacks</h4>
Guarentee Bandwidth for a particular flow.
![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/Screen Shot 2016-06-14 at 10.02.37 PM.png)

<h4> Reflector Attacks</h4>
Allow Connections to only a range of ports.
![](https://raw.githubusercontent.com/sivaramakrishnansr/ISPSecurity/master/Screen Shot 2016-06-17 at 11.21.56 AM.png)
