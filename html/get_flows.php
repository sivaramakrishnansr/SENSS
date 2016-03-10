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
                                        <li><a href="pic.php">View</a></li>
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
							if($key=="tcp_src" || $key=="tcp_dst"){
								$match_list["ip_proto"]=6;
							}
							if($key=="udp_src" || $key=="udp_dst"){
								$match_list["ip_proto"]=17;
							}
						}
					}
					$data_to_send=array();
					if (count($match_list)!=0){
						$dpid = $_POST['dpid'];
						$data_to_send["match"]=$match_list;
						$data_string = json_encode($data_to_send);
                				$url='http://192.168.0.9:8080/stats/flow/'.$dpid;
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
						$json_data=json_encode($json_output);
						foreach($json_output[$dpid] as $key){
 							echo "Byte Count-".$key["byte_count"]." "."Packet Count-".$key["packet_count"]." "."In Port-".$key["match"]["in_port"];
							echo "<br/>";
						}
					}
					else{
						$dpid = $_POST['dpid'];
                				$url='http://192.168.0.9:8080/stats/flow/'.$dpid;
                				$ch=curl_init($url);
						curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	        				$result = curl_exec($ch);
                				curl_close($ch);
                				$json_output = json_decode($result,true);
						$json_data=json_encode($json_output);
						foreach($json_output[$dpid] as $key){
 							echo "Byte Count-".$key["byte_count"]." "."Packet Count-".$key["packet_count"]." "."In Port-".$key["match"]["in_port"];
						echo "<br/>";
						}
					}
					echo '<h1>Got Flows-'.$dpid.'</h1>';
			        }
  		?>
	</table>
</body>
</html>
