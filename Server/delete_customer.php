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
          <title>SENSS - Delete Customer</title>
          <link rel="stylesheet" href="css/bootstrap.min.css">
          <script src="css/jquery.min.js"></script>
          <script src="css/bootstrap.min.js"></script>
          <style>
                .panel { width:300px; margin:auto; padding: 30px;}
                .panel-offset-senss { margin:auto;}
          </style> 
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
		//Customer E2 91 5C 19 8E E7 38 49 4C 80 11 D4 43 C5 A4 5B BA 3C 0C 1A
		//Server 60 D1 DA E3 3E 61 02 10 AF 0B 6F 4C F6 52 88 91 9C 16 C3 9B

		if($_POST['formSubmit'] == "Delete"){
			$customer_id=$_POST['customer_id'];
			$servername = "localhost";
                	$username = "root";
                	$password = "usc558l";
                	$dbname = "SENSS";

                	$conn = new mysqli($servername, $username, $password, $dbname);
                	if ($conn->connect_error) {
                        	die("Connection failed: " . $conn->connect_error);
                	}
			$sql = "DELETE FROM SENSS_CUSTOMERS WHERE ID=".$customer_id;
                	if ($conn->query($sql) === FALSE) {
                        	echo "Error: " . $sql . "<br>" . $conn->error;
                	}
                	$conn->close();
			header("Location: http://localhost:8118/server/view_customer.php"); /* Redirect browser */
			exit();
		}

	?>
        </div>


</body>
</html>
