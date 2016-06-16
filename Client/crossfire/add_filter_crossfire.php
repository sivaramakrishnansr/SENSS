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

		//Adding flow from 1 to 2
		$data_to_send=array();
		$data_to_send["dpid"]=$dpid;
		$match_list["in_port"]=1;
		$match_list["dl_type"]=2048;
		$data_to_send["match"]=$match_list;
                $temp_array=array();
                $temp_array["type"]="OUTPUT";
                $temp_array["port"]=2;
                $data_to_send["actions"]=array($temp_array);
		$data_string = json_encode($data_to_send);
                $url='http://192.168.0.125:8080/stats/flowentry/add';
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
		echo "Flow1".$result."\n";

		//Adding flow from 2 to 1
		$data_to_send=array();
		$data_to_send["dpid"]=$dpid;
		$data_to_send["priority"]=100;
		$match_list["in_port"]=2;
		$match_list["eth_type"]=2048;
		$data_to_send["match"]=$match_list;
                $temp_array=array();
                $temp_array["type"]="OUTPUT";
                $temp_array["port"]=1;
                $data_to_send["actions"]=array($temp_array);
                $data_string = json_encode($data_to_send);
		$url='http://192.168.0.125:8080/stats/flowentry/add';
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
		echo "Flow2".$result."\n";

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
		$sql ="SELECT * FROM CROSSFIRE WHERE ID='$request_id'";
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
		$sql="UPDATE CROSSFIRE SET FILTER='$filter' WHERE ID='$request_id'";
		echo $sql;
                $result = $conn->query($sql);
		echo '<br />';
		echo '<h1>Flow Added-'.$dpid.'</h1>';
		header("Location: http://localhost:8118/crossfire_view.php"); 
		exit();
	}
  ?>
</table>

</body>
</html>
