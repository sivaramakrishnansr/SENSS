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

                $ip_filter = $_POST['ip_filter'];
		$dpid = $_POST['dpid'];
		$data_string = json_encode($data_to_send);
                $url='http://192.168.0.125:8080/stats/flowentry/clear/'.$dpid;
                $ch=curl_init($url);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	        $result = curl_exec($ch);
                curl_close($ch);

        }
  ?>
</table>

</body>
</html>
