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
		$match_list=array();
		foreach ($_POST as $key => $value) {
			if($key=="dpid"){
				$dpid=$value;
				continue;
			}
			if(strlen($value)!=0 && $value!=Submit){

				$match_list[$key]=$value;
				if($key=="tcp_src" || $key=="tcp_dst"){
					$match_list["ip_proto"]=6;
				}
				if($key=="udp_src" || $key=="udp_dst"){
					$match_list["ip_proto"]=17;
				}

			}
		}


                $ip_filter = $_POST['ip_filter'];
                $dpid = $_POST['dpid'];
                $data_string = json_encode($data_to_send);
                $url='http://controller.dhs.senss:8080/stats/flowentry/clear/'.$dpid;
                $ch=curl_init($url);
                curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                $result = curl_exec($ch);
                curl_close($ch);


                $data_to_send=array();
                $data_to_send["dpid"]=$dpid;
                $data_to_send["priority"]=0;

                $match_list["in_port"]=2;
                //$match_list["eth_type"]=2048;
                $data_to_send["match"]=$match_list;
		$temp_array=array();
		$temp_array["type"]="OUTPUT";
		$temp_array["port"]=1;
                $data_to_send["actions"]=array($temp_array);
		print_r($data_to_send);
                $ip_filter = $_POST['ip_filter'];
                $dpid = $_POST['dpid'];
                $data_string = json_encode($data_to_send);
                $url='http://controller.dhs.senss:8080/stats/flowentry/add';
                $ch=curl_init($url);
                curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
                curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_HTTPHEADER, array(
                        'Content-Type: application/json',
                        'Content-Length: ' . strlen($data_string))
                );
                $result = curl_exec($ch);
                curl_close($ch);
                $data_to_send=array();
                $data_to_send["dpid"]=$dpid;
                $data_to_send["priority"]=0;

                $match_list["in_port"]=1;
                //$match_list["eth_type"]=2048;
                $data_to_send["match"]=$match_list;
		$temp_array=array();
		$temp_array["type"]="OUTPUT";
		$temp_array["port"]=2;
                $data_to_send["actions"]=array($temp_array);
		print_r($data_to_send);
                $ip_filter = $_POST['ip_filter'];
                $dpid = $_POST['dpid'];
                $data_string = json_encode($data_to_send);
                $url='http://controller.dhs.senss:8080/stats/flowentry/add';
                $ch=curl_init($url);
                curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
                curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
                curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($ch, CURLOPT_HTTPHEADER, array(
                        'Content-Type: application/json',
                        'Content-Length: ' . strlen($data_string))
                );
                $result = curl_exec($ch);
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
		$filter=explode(",",$filter);
		$filter=array_diff($filter,array($dpid));
		$filter=implode(",",$filter);
		$sql="UPDATE DIRECT_FLOODS SET FILTER='$filter' WHERE ID='$request_id'";
		echo $sql;
                $result = $conn->query($sql);
		echo '<br />';
		echo '<h1>Filter Removed-'.$dpid.'</h1>';
                $date=new DateTime();
                $date_time = $date->format('Y-m-d H:i:s');
                $sql="INSERT INTO SENSS_LOGS(REQUEST_TYPE,REQUEST_FROM,TIME,RESPONSE) VALUES ('remove_traffic_filter','Winston','$date_time','Filter Removed')";
                $result = $conn->query($sql);

                header("Location: http://localhost:8118/client/crossfire_view.php"); 
                exit();
		//Connect to the database and add the flow

        }
  ?>
</table>

</body>
</html>
