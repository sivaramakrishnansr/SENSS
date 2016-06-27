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
          <title>SENSS - Crossfire</title>
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
                                <a class="navbar-brand" href="direct_floods_form.php">SENSS-CLIENT</a>
                        </div>
                        <div>
                                <ul class="nav navbar-nav">
                                        <li><a href="direct_floods_form.php">Direct Floods</a></li>
                                        <li><a href="crossfire_form.php">Crossfire</a></li>
                                        <li><a href="reflector_view.php">Reflector</a></li>
                                </ul>
                                </a>
                        </div>
                </div>
        </nav>
 <form>

<table>
 <?php
	if($_POST['formSubmit'] == "Submit")
        {
		$o_time= $_POST['o_time'];
		$tag=$_POST['tag'];
		$total_times=$_POST['total_times'];
        	$isp=$_POST['isp'];
        }

        $servername = "localhost";
        $username = "root";
        $password = "usc558l";
       	$dbname = "SENSS";
        $conn = new mysqli($servername, $username, $password, $dbname);

        if ($conn->connect_error) {
               die("Connection failed: " . $conn->connect_error);
	}
	$done=0;
        $sql = "INSERT INTO DIRECT_FLOODS (ID,REQUEST_TO,O_TIME,TOTAL_TIMES,TAG,DONE) VALUES (NULL, '$isp','$o_time','$total_times','$tag','$done')";
	if ($conn->query($sql) === FALSE) {
               echo "Error: " . $sql . "<br>" . $conn->error;
        }
        $conn->close();
	echo "<h1> Waiting for Results</h1>";
	sleep (10);
	header("Location: http://localhost:8118/client/crossfire_view.php");
	exit();

  ?>
</table>

</body>
</html>
