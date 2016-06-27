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
	  <title>SENSS - Remove Switch</title>
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
	<div class="panel panel-default panel-offset-senss">
	<form action="remove_switch.php" method="post">
			<div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="switch_ip" id="switch_ip" maxlength="50"  placeholder="IP Address of Switch" />
                        </div>
			<div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="switch_username" id="switch_username" maxlength="50"  placeholder="Switch Username" />
                        </div>
			<div class="form-group">
                                <input type="password" style="width:200px;" class="form-control" name="switch_password" id="switch_password" maxlength="50"  placeholder="Switch Password" />
                        </div>
			<input type="submit" name="formSubmit" class="btn" value="Submit" />
	</form>
	</div>

</body>
</html>
