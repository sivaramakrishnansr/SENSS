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
    .second-button{
			   float:right;
       }
     </style>
</head>

<body>
<nav class="navbar navbar-inverse navbar-static-top">
  <div class="container-fluid">
    <div class="navbar-header">
      <a class="navbar-brand" href="direct_floods_form.php">SENSS|Proxy</a>
    </div>
    <div>
      <ul class="nav navbar-nav">
        <li><a href="direct_floods_form.php">Direct Floods</a></li>
      </ul>
    </div>
  </div>
</nav>

<center>
  <img src="demo_proxy.png" width="100%" height="100%">
</center>

<br />
<br />
<br />

<?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "SENSS";
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT * FROM DIRECT_FLOODS";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $proxy=$row["PROXY"];
            $attack=$row["ATTACK"];
            if ($proxy=="1" && $attack=="1") {
                echo '<div class="alert alert-info">';
                echo '<strong>Info:</strong> At SENSS proxy at ICN';
                echo '</div>';
                echo '<div class="alert alert-danger">';
                $attack_from=$row["ATTACK_FROM"];
                echo '<strong>Info:</strong> Attack traffic from '.$attack_from;
                echo '</div>';
                echo '<div class="alert alert-info">';
                echo '<strong>Info:</strong> Request SENSS ISP to add filters below.';
                echo '</div>';
            }
            if ($proxy=="1" && $attack=="0") {
                echo '<div class="alert alert-info">';
                echo '<strong>Info:</strong> SENSS ISP at ARNEP,EQUINIX and INTERNEXA';
                echo '</div>';
                echo '<div class="alert alert-info">';
                echo '<strong>Info:</strong> Legit traffic from UEM and ENTEL';
                echo '</div>';
            }
            $result=json_decode($row["RESULT"], true);
            echo '<table  class="table table-striped" align="center" style="width: auto;">';
            echo '<tr><th>DPID</th><th>Action</th><th>Stop Action</th></tr>';
            foreach ($result as $dpid=>$count) {
                $dpid_of_switch=$count["DPID"];
                $isp_of_switch=$count["ISP"];
                $filter=explode(",", $row["FILTER"]);
                $remove_action=false;
                foreach ($filter as $filter_dpid) {
                    if ($filter_dpid==$dpid_of_switch) {
                        $remove_action=true;
                    }
                }
                if ($count["Mark"] == "True") {
                    if ($remove_action==true) {
                        echo '<tr><td>'.$isp_of_switch.'</td><td></td><td><button type="button" class="btn btn-danger" data-toggle="modal" data-target="#Remove-'.$dpid.'">Remove Filter</button></td></tr>';
                        echo '<div id="Remove-'.$dpid.'" class="modal fade" role="dialog">';
                        echo '<div class="modal-dialog">';
                        echo '<div class="modal-content">';
                        echo '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button>';
                        echo '<h4 class="modal-title">Remove Filter</h4>';
                        echo '</div>';
                        echo '<div class="modal-body">';
                        echo '<form name="remove_filter_form" id="remove_filter_form" action="remove_filter.php" method="post">';
                        echo '<h3> Are you sure you want to remove this filter?</h3>';
                        echo '<input type="hidden" name="request_id" value="'.$row["ID"].'"/>';
                        echo '<input type="hidden" name="dpid" value="'.$dpid_of_switch.'"/>';
                        echo '<input type="submit" class="btn" name="formSubmit" value="Submit"/> ';
                        echo '</form> ';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                    } else {
                        echo '<tr><td>'.$isp_of_switch.'</td>'.'<td><button type="button" class="btn btn-danger" data-toggle="modal" data-target="#Add-'.$dpid.'">Add Filter</button></td><td></td></tr>';
                    }
                    echo '<div id="Add-'.$dpid.'" class="modal fade" role="dialog">';
                    echo '<div class="modal-dialog">';
                    echo '<div class="modal-content">';
                    echo '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button>';
                    echo '<h4 class="modal-title">Add Filter</h4>';
                    echo '</div>';
                    echo '<div class="modal-body">';
                    echo '<form name="add_filter_form" id="add_filter_form" action="add_filter_proxy.php" method="post">';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="dpid" id="dpid" maxlength="50"  readonly="readonly" value="'.$dpid_of_switch.'" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="nw_src" id="nw_src" maxlength="50"  placeholder="Source IP" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="nw_dst" id="nw_dst" maxlength="50"  placeholder="Destination IP" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="in_port" id="in_port" maxlength="50"  placeholder="In Port" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="eth_dst" id="eth_dst" maxlength="50"  placeholder="Destination MAC" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="eth_src" id="eth_src" maxlength="50"  placeholder="Source MAC" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="dl_vlan" id="dl_vlan" maxlength="50"  placeholder="VLAN ID" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="tcp_src" id="tcp_src" maxlength="50"  placeholder="TCP Source Port" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="tcp_dst" id="tcp_dst" maxlength="50"  placeholder="TCP Destination Port" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="udp_src" id="udp_src" maxlength="50"  placeholder="UDP Source Port" />';
                    echo '</div>';
                    echo '<div class="form-group">';
                    echo '<input type="text" style="width:200px;" class="form-control" name="udp_dst" id="udp_dst" maxlength="50"  placeholder="UDP Destination Port" />';
                    echo '</div>';
                    echo '<input type="hidden" name="request_id" value="'.$row["ID"].'"/>';
                    echo '<input type="submit" class="btn" name="formSubmit" value="Submit"/> ';
                    echo '</form> ';
                    echo '</div>';
                    echo '</div>';
                    echo '</div>';
                    echo '</div>';
                } else {
                    if ($remove_action==true) {
                        echo '<tr><td>'.$isp_of_switch.'</td><td></td><td><button type="button" class="btn btn-danger" data-toggle="modal" data-target="#Remove-'.$dpid.'">Remove Filter</button></td></tr>';
                        echo '<div id="Remove-'.$dpid.'" class="modal fade" role="dialog">';
                        echo '<div class="modal-dialog">';
                        echo '<div class="modal-content">';
                        echo '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button>';
                        echo '<h4 class="modal-title">Add Filter</h4>';
                        echo '</div>';
                        echo '<div class="modal-body">';
                        echo '<form name="remove_filter_form" id="remove_filter_form" action="remove_filter_proxy.php" method="post">';
                        echo '<h3> Are you sure you want to remove this filter?</h3>';
                        echo '<input type="hidden" name="request_id" value="'.$row["ID"].'"/>';
                        echo '<input type="hidden" name="dpid" value="'.$dpid_of_switch.'"/>';
                        echo '<input type="submit" class="btn" name="formSubmit" value="Submit"/> ';
                        echo '</form> ';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                        echo '</div>';
                    } else {
                        echo '<tr><td>'.$isp_of_switch.'</td><td></td><td></td></tr>';
                    }
                }
            }
        }
    }
?>
</body>
</html>
