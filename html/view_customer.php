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
                                <a class="navbar-brand" href="index.php">SENSS</a>
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
	        $servername = "localhost";
        	$username = "root";
        	$password = "";
        	$dbname = "SENSS";
	        $conn = new mysqli($servername, $username, $password, $dbname);
       	 	if ($conn->connect_error) {
                	die("Connection failed: " . $conn->connect_error);
        	}
		$sql = "SELECT * FROM SENSS_CUSTOMERS";
		$result = $conn->query($sql);
		if ($result->num_rows > 0) {
		    echo '<table  class="table table-striped" align="center" style="width: auto;">';
		    echo '<tr><th>Customer Name</th><th> IP </th><th> Public Key </th> <th> RPKI </th>  </tr>';
		    while($row = $result->fetch_assoc()) {
			echo "<tr>";
			if($row["RPKI"]=="1"){
				$rpki="True";
			}
			else{
				$rpki="False";
			}
			$value=$row["ID"];
        		echo "<td>" . $row["CUSTOMER_NAME"]. "</td><td>"  . $row["IP"]. "</td><td> " . $row["PUBLIC_KEY"]. "</td><td>" .$rpki. "</td>";
			echo '<form action="delete_customer.php" method="post">';
			echo '<input type="hidden" name="customer_id" value='.$value.' />';
			echo '<td><input type="submit" name="formSubmit" class="btn" value="Delete" /></td>';
			echo "</form>";
			echo "</tr>";

    		   }
		   echo "</table>";
		}
		else{
		echo "<h1>No customers found</h1>";
		}

	?>
</body>
</html>
