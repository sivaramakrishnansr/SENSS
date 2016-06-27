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

<div class="panel panel-default">
        <div class="panel-offset-senss">
                <form name="add_filter_form" id="add_filter_form" action="add_filter.php" method="post">
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="nw_src" id="nw_src" maxlength="50"  placeholder="Source IP" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="nw_dst" id="nw_dst" maxlength="50"  placeholder="Destination IP" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="in_port" id="in_port" maxlength="50"  placeholder="In Port" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="eth_dst" id="eth_dst" maxlength="50"  placeholder="Destination MAC" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="eth_src" id="eth_src" maxlength="50"  placeholder="Source MAC" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="dl_vlan" id="dl_vlan" maxlength="50"  placeholder="VLAN ID" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="tcp_src" id="tcp_src" maxlength="50"  placeholder="TCP Source Port" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="tcp_dst" id="tcp_dst" maxlength="50"  placeholder="TCP Destination Port" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="udp_src" id="udp_src" maxlength="50"  placeholder="UDP Source Port" />
                        </div>
                        <div class="form-group">
                                <input type="text" style="width:200px;" class="form-control" name="udp_dst" id="udp_dst" maxlength="50"  placeholder="UDP Destination Port" />
                        </div>


		        <?php
                		$url='http://controller.dhs.senss:8080/stats/switches';
                		$ch=curl_init($url);
               	 		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                		$result = curl_exec($ch);
                		curl_close($ch);
                		$json_output = json_decode($result,true);
                		$switch_count=0;
                		echo '<label>Select ISP:</label>';
                		echo '<select class="form-control" name="dpid">';
                		foreach($json_output as $item){
                        		$switch_dpid=$item;
                        		$switch_count=$switch_count+1;
                        		$command='python /var/www/html/scripts/dpid_to_city.py '.$switch_dpid.' 2>&1';
                        		$switch_name=trim(shell_exec($command));
                        		echo '<option value="'.$switch_dpid.'">'.$switch_name.'</option>';
                		}
                		echo '</select>';
		        ?>
			<br />
                        <input type="submit" class="btn" name="formSubmit" value="Submit"/>
                </form>
        </div>
</div>


</body>
</html>
