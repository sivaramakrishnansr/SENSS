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
	<div class="panel panel-default">
        	<div class="panel-offset-senss">
                	<form name="get_routes_form" id="get_routes_form" action="get_routes.php" method="post">
                        	<div class="form-group">
		        	<?php
                				$url='http://192.168.0.9:8080/stats/switches';
                				$ch=curl_init($url);
               	 				curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                				$result = curl_exec($ch);
                				curl_close($ch);
                				$json_output = json_decode($result,true);
                				$switch_count=0;
                				echo '<label>Select Source ISP:</label>';
                				echo '<select class="form-control" name="source_isp">';
                				foreach($json_output as $item){
                        				$switch_dpid=$item;
                        				$switch_count=$switch_count+1;
                        				$command='python /var/www/html/scripts/dpid_to_city.py '.$switch_dpid.' 2>&1';
                        				$switch_name=trim(shell_exec($command));
                        				echo '<option value="'.$switch_dpid.'">'.$switch_name.'</option>';
                				}
                				echo '</select>';
		        	?>
				</div>
	                        <div class="form-group">
			        <?php
                				$url='http://192.168.0.9:8080/stats/switches';
                				$ch=curl_init($url);
               	 				curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                				$result = curl_exec($ch);
                				curl_close($ch);
                				$json_output = json_decode($result,true);
                				$switch_count=0;
                				echo '<label>Select Destination ISP:</label>';
              			  		echo '<select class="form-control" name="destination_isp">';
                				foreach($json_output as $item){
                        				$switch_dpid=$item;
                        				$switch_count=$switch_count+1;
                        				$command='python /var/www/html/scripts/dpid_to_city.py '.$switch_dpid.' 2>&1';
                        				$switch_name=trim(shell_exec($command));
                        				echo '<option value="'.$switch_dpid.'">'.$switch_name.'</option>';
                				}
                				echo '</select>';
		        	?>
				</div>
				<br />
	                        <input type="submit" class="btn" name="formSubmit" value="Submit!"/>
                </form>
        </div>
</div>
</body>
</html>
