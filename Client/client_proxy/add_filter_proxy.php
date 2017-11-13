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
          <title>My Form</title>
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
                                        <li><a href="pic.php">View</a></li>
					<li><a href="direct_floods_form.php">Direct Floods</a></li>
                                </ul>
                        </div>
                </div>
        </nav>
 <form>

<table>
<?php
        if($_POST['formSubmit'] == "Submit")
        {
		$match_list=array();
		foreach ($_POST as $key => $value) {
			if($key=="dpid"){
				$dpid=$value;
				continue;
			}

			if(strlen($value)!=0 && $value!=Submit){
				$match_list[$key]=$value;
			}
		}

                $ip_filter = $_POST['ip_filter'];
		$dpid = $_POST['dpid'];
		$data_string = json_encode($data_to_send);
                $url='http://localhost:8080/stats/flowentry/clear/'.$dpid;
		echo $url."\n";
                $ch=curl_init($url);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	        $result = curl_exec($ch);
		echo $result;
                curl_close($ch);



                $json_output = json_decode($result,true);
		$results_to_store=$dpid;
                $servername = "localhost";
                $username = "root";
                $password = "usc558l";
                $dbname = "SENSS";
                $conn = new mysqli($servername, $username, $password, $dbname);
		$request_id=$_POST["request_id"];
                if ($conn->connect_error) {
                        die("Connection failed: " . $conn->connect_error);
                }
		$sql ="SELECT * FROM DIRECT_FLOODS WHERE ID='$request_id'";
                $result = $conn->query($sql);
		 while($row = $result->fetch_assoc()) {
			if (strlen($row["FILTER"])!=0){
				$filter=$row["FILTER"];
			}
			else{
				$filter="";
			}
		}
		if (strlen(filter)!=0){
			$filter=$filter.",".$results_to_store;
		}else{
			$filter=$results_to_store;
		}
		$sql="UPDATE DIRECT_FLOODS SET FILTER='$filter' WHERE ID='$request_id'";
		echo $sql;
                $result = $conn->query($sql);
		echo '<br />';
		echo '<h1>Flow Added-'.$dpid.'</h1>';

		$date=new DateTime();
		$date_time = $date->format('Y-m-d H:i:s');
		$sql="INSERT INTO SENSS_LOGS(ID,REQUEST_TYPE,REQUEST_FROM,TIME,OUTPUT) VALUES (0,'add_traffic_filter','LBMC','$date_time','Filter Added')";
                $result = $conn->query($sql);

		header("Location: http://localhost:8181/direct_floods_multiple_view_proxy.php"); 
		exit();
        }
  ?>
</table>
</body>
</html>
