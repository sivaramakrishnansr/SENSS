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
  	  <style>
                .panel { width:300px; margin:auto; padding: 30px;}
                .panel-offset-senss { margin:auto;}
          </style> 
</head>

<body>
        <nav class="navbar navbar-inverse navbar-static-top">
                <div class="container-fluid">
                        <div class="navbar-header">
                                <a class="navbar-brand" href="index.php">SENSS</a>
                        </div>
                        <div>
                                <ul class="nav navbar-nav">
                                        <li><a href="add_filter_form.php">Add Filter</a></li>
                                        <li><a href="get_flows_form.php">Flow Stats</a></li>
                                        <li><a href="get_routes_form.php">Route Stats</a></li>
					<li><a href="direct_floods_form.php">Direct Floods</a></li>
                                        <li><a href="pic.php">View</a></li>
                                </ul>
                        </div>
                </div>
        </nav>
 <form>

<table>
	 <?php
	        if($_POST['formSubmit'] == "Submit!")
        	{
			echo exec('whoami');
			$source_isp=$_POST['source_isp'];
			$destination_isp=$_POST['destination_isp'];
			$command_to_execute="sudo python /var/www/html/scripts/get_routes.py ".$source_isp." ".$destination_isp." 2>&1";
			$route_output=shell_exec($command_to_execute);
			$command_to_execute="sudo python /var/www/html/scripts/plot.py ".$source_isp." ".$destination_isp." 2>&1";
			$route_output=shell_exec($command_to_execute);
			header("Location: http://localhost:8118/pic.php"); /* Redirect browser */
			exit();
        	}
  	?>
</table>
</body>
</html>
