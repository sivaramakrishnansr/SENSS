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
          <title>SENSS</title>
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
                                <a class="navbar-brand" href="index.php">SENSS-ISP</a>
                        </div>
                        <div>
                                <ul class="nav navbar-nav">
                                        <li><a href="add_switch_form.php">Add Switch</a></li>
                                        <li><a href="get_switch.php">List Switches</a></li>
                                        <li><a href="remove_switch_form.php">Remove Switch</a></li>
                                        <li><a href="logs.php">Logs</a></li>
                                </ul>
                        </div>
                </div>
        </nav>
	<?php
	if($_POST['formSubmit'] == "Submit")
	{
        	$customer_name = $_POST['customer_name'];
		$ip_prefixes = $_POST['ip_prefixes'];
		$public_key = $_POST['public_key'];
        	$rpki_validation = $_POST['rpki_validation'];
		if($rpki_validation=="on"){
			$rpki="1";
		}
		else{
			$rpki="0";
		}
		$servername = "localhost";
	        $username = "root";
        	$password = "";
        	$dbname = "SENSS";

        	$conn = new mysqli($servername, $username, $password, $dbname);
        	if ($conn->connect_error) {
                	die("Connection failed: " . $conn->connect_error);
        	}
	        $sql = "INSERT INTO SENSS_CUSTOMERS (ID,CUSTOMER_NAME,IP,PUBLIC_KEY,RPKI) VALUES (NULL, '$customer_name','$ip_prefixes','$public_key','$rpki')";
        	if ($conn->query($sql) === FALSE) {
                	echo "Error: " . $sql . "<br>" . $conn->error;
        	}
        	$conn->close();
		echo "<h1>Added Customer</h1>";
                header("Location: http://localhost:8118/view_customer.php"); /* Redirect browser */
                exit();

	}
	?>
</body>
</html>
