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
          <title>Reflector</title>
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
					<li><a href="direct_floods_form.php">Direct Floods</a></li>
					<li><a href="crossfire_form.php">Crossfire</a></li>
					<li><a href="reflector_form.php">Reflector</a></li>
                                </ul>
                        </div>
                </div>
        </nav>
	<div class="panel panel-default">
        	<div class="panel-offset-senss">
				<div class="form-group">
					<center><button type="button" class="btn btn-danger" data-toggle="modal" data-target="#Add-Filter">Add Filter</button></center>
                        	</div>
        	</div>
	</div>

	<?php
		$dpid_of_switch=23;
 		echo '<div id="Add-Filter" class="modal fade" role="dialog">';
			   echo '<div class="modal-dialog">';
			 	echo '<div class="modal-content">';
		 			echo '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button>';
                                             	echo '<h4 class="modal-title">Add Allowed Ports</h4>';
                                        echo '</div>';
					echo '<div class="modal-body">';
					        echo '<form name="add_filter_reflector_form" id="add_filter_reflector_form" action="add_filter_reflector.php" method="post">';
							echo '<div class="form-group">';
                                               			echo '<input type="text" style="width:200px;" class="form-control" name="dpid" id="dpid" maxlength="50"  readonly="readonly" value="'.$dpid_of_switch.'" />';
                                            		echo '</div>';
                                                	echo '<div class="form-group">';
                                                			echo '<input type="text" style="width:200px;" class="form-control" name="in_port" id="in_port" maxlength="50"  placeholder="In Port" />';
                                                	echo '</div>';
                                                	echo '<input type="submit" class="btn" name="formSubmit" value="Submit"/> ';
                                                 echo '</form> ';
					echo '</div>';
				echo '</div>';
			echo '</div>';
		echo '</div>';
	?>
	</body>
</html>
