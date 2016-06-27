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
          <title>SENSS - Reflector</title>
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
				echo $key." ".$value."\n";
			}
		}
		$match_list["nw_proto"]=6;
		$match_list["dl_type"]=2048;
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
        }
  ?>
</table>

</body>
</html>
