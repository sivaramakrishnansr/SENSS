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
          <title>SENSS - Add Customer</title>
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
        <form action="add_customer.php" method="post">
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="customer_name" id="customer_name" maxlength="50"  placeholder="Customer Name" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="ip_prefixes" id="ip_prefixes" maxlength="5000"  placeholder="IP Prefixes(CSV)" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="public_key" id="public_key" maxlength="150"  placeholder="Public Key" />
                        </div>
			<div class="form-group">
				<input type="checkbox" name="rpki_validation">

				RPKI Validation
			</div>
                        <input type="submit" name="formSubmit" class="btn" value="Submit" />
        </form>
        </div>


</body>
</html>
