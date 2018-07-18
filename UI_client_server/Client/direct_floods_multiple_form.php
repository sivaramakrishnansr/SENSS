<!--
#
# Copyright (C) 2018 University of Southern California.
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
                                <a class="navbar-brand" href="direct_floods_multiple_form.php">SENSS</a>
                        </div>
                        <div>
                                <ul class="nav navbar-nav">
					<li><a href="direct_floods_form.php">Direct Floods</a></li>
                                        <li><a href="direct_floods_view.php">View</a></li>
                                        <li><a href="crossfire_form.php">Crossfire</a></li>
                                </ul>
                        </div>
                </div>
        </nav>


<div class="panel panel-default">
        <div class="panel-offset-senss">
                <form name="direct_floods_form" id="direct_floods_form" action="direct_floods_multiple.php" method="post">
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="o_time" id="o_time" maxlength="50"  placeholder="Observation Time" />
                        </div>
                        <!--<div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="total_times" id="total_times" maxlength="50"  placeholder="Total Requests" />
                        </div>-->
			<div class="form-group">
                		<label>Tag:</label>
                		<select class="form-control" name="tag">
                        		<option value="IN">IN</option>
                        		<option value="OUT">OUT</option>
                        		<option value="SELF">SELF</option>
                		</select>
			</div>
			<br />
                        <input type="submit" class="btn" name="formSubmit" value="Submit"/>
                </form>
        </div>
</div>


</body>
</html>
