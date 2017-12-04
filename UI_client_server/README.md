## Client GUI

### Database Setup

**Prerequisites:** Python, MySQL and mysql-python

Open Database/init.py file and enter your database password in the "password" field. Run the python script using the following command:

    $ python init.py
    
The python script will create two databases - one for SENSS Server and the other for SENSS Client, and add the required tables.

Edit the Database configuration files Client/db_conf.php and Server/db.php to include your database configuration for both SENSS server and client. For more information regarding database tables and its fields, please see the database documentation [here](https://github.com/sivaramakrishnansr/SENSS/tree/master/UI_client_server/Database)
 
### SENSS Servers Setup

You may add SENSS Servers to the Database by inserting records to the table AS_URLS in the database SENSS_CLIENT.

**Note:** Please add Client's AS details to the AS_URLS table as well, and set the "self" flag for the client AS.

You may add a SENSS server by running the following MySQL query:

    INSERT INTO AS_URLS (as_name, server_url, self) VALUES ("ISI-AS", "senss.isi.edu", 1);

### Launch GUI

To launch Client GUI, launch Client/direct_floods_multiple_view.php from your web browser.

You will see a rendered topology with all the SENSS Servers like the image below:

![Initial_topology](https://github.com/sivaramakrishnansr/SENSS/raw/master/UI_client_server/screenshots/initial.png)

You may set the threshold for the SENSS Client, by clicking the "Edit" option besides the Threshold field. A dialog will appear as below:

![Set_Threshold](https://github.com/sivaramakrishnansr/SENSS/raw/master/UI_client_server/screenshots/2_set_threshold.png)

To add monitor(s) to SENSS Servers, click the "Add Monitoring Rule" option, specify the SENSS Servers where a monitor is to be added, and enter the monitor parameters/filters:
 
![Add_Monitor](https://github.com/sivaramakrishnansr/SENSS/raw/master/UI_client_server/screenshots/3_add_monitoring_rule.png)

A table will populate with the monitoring values from the SENSS Servers you requested monitoring data. The values are refreshed every x seconds provided in the "Monitoring Frequency" field while adding the monitoring rule.

![Monitoring](https://github.com/sivaramakrishnansr/SENSS/raw/master/UI_client_server/screenshots/4_monitoring.png)

The inbound traffic metric (speed) will also appear in the topology view with the green color indicating the traffic is below the specified threshold, and red indicating the opposite.
 
You may add a filter to any of the SENSS Server for traffic coming to your AS, by selecting the option "Add Filter". Traffic coming from that AS will be filtered.

![Add_Filter](https://github.com/sivaramakrishnansr/SENSS/raw/master/UI_client_server/screenshots/5_add_filter.png)
