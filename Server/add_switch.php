<!--

#
# Copyright (C) 2016 University of Southern California.
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
-->
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<html>
<head>
          <title>SENSS - Add Switch</title>
          <link rel="stylesheet" href="css/bootstrap.min.css">
          <script src="css/jquery.min.js"></script>
          <script src="css/bootstrap.min.js"></script>
          <script src="css/jquery.form.js"></script>
          <script src="css/jquery.js"></script>
</head>

<body>
        <nav class="navbar navbar-inverse navbar-static-top">
                <div class="container-fluid">
                        <div class="navbar-header">
                                <div class="navbar-brand">SENSS-SERVER</div>
                        </div>
                        <div>
                                <ul class="nav navbar-nav">
                                        <li><a href="add_switch_form.php">Add Switch</a></li>
                                        <li><a href="get_switch.php">List Switches</a></li>
                                        <li><a href="remove_switch_form.php">Remove Switch</a></li>
                                        <li><a href="logs.php">Logs</a></li>
                                        <li><a href="add_customer_form.php">Add Customer</a></li>
                                        <li><a href="view_customer.php">View Customer</a></li>
                                        <li><a href="http://localhost/index.php">Log Out</a></li>
                                </ul>
                        </div>
                </div>
        </nav>
	<?php
	if($_POST['formSubmit'] == "Submit")
	{
        	$switch_ip = $_POST['switch_ip'];
		$switch_username=$_POST['switch_username'];
		$switch_password=$_POST['switch_password'];
        	$controller_ip = $_POST['controller_ip'];
        	$controller_port = $_POST['controller_port'];
		include('Net/SSH2.php');
		$ssh = new Net_SSH2($switch_ip);
		if (!$ssh->login($switch_username, $switch_password)) {
    			exit('Login Failed!');
		}
		$command_to_exec='sudo python /proj/SENSS/config_switch.py '.$controller_ip.' '.$controller_port;
		$return_value=$ssh->exec($command_to_exec);
		echo("<h1>Added the switch</h1>");
	}
	?>
</body>
</html>
