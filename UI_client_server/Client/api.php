<?php
function display_threshold($int_threshold) {
        $zeros = log($int_threshold) / log(10);
        if ($zeros >= 12) {
                return round($int_threshold / pow(10, 12),2)." TBps";
        } else if ($zeros >= 9) {
                return round($int_threshold / pow(10, 9),2)." GBps";
        } else if ($zeros >= 6) {
                return round($int_threshold / pow(10, 6),2)." MBps";
        } else if ($zeros >= 3) {
                return round($int_threshold / pow(10, 3),2)." KBps";
        } else {
                return $int_threshold." Bps";
        }
}

function generate_request_headers() {
    $clientcert = file_get_contents('/var/www/html/SENSS/UI_client_server/Client/cert/clientcert.pem');
    $clientcert = base64_encode($clientcert);
    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
}

//Adding the topology
//Add filter all used by DDoS with Signature to add filters to all monitoring nodes
if (isset($_GET["add_topo"])){
    	$input = file_get_contents("php://input");
    	$input = json_decode($input, true);
//if (1){
/*	$input=array(
		"as_name"=>"H",
		"server_url"=>"html",
		"links_to"=>"asdasd",
		"self"=>1
	);*/
	require_once "db_conf.php";
	$sql = sprintf("INSERT INTO AS_URLS (as_name, server_url, links_to, self) VALUES ('%s', '%s', '%s', %d)", $input['as_name'], $input['server_url'], $input['links_to'], $input['self']);
	$conn->query($sql);
	$conn->commit();
	return;
}

//Function used for testing purpose
//if(isset($_GET['check'])){
if(1){
    	require_once "db_conf.php";
    	$sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    	$result = $conn->query($sql);
    	$all_urls=array();
    	while ($row = $result->fetch_assoc()) {
       	 	$as_name=$row["as_name"];
        	$monitor_id=$row["monitor_id"];
		$temp=array($as_name=>$monitor_id);
		array_push($all_urls,$temp);
   	}
    	$url = "http://56.0.0.1/SENSS/UI_client_server/Proxy/api.php?action=proxy_info";
    	$url = "http://56.0.0.1/SENSS/UI_client_server/Proxy/api.php?action=get_nonce";
        $data_string = json_encode($all_urls,true);

        $response = file_get_contents($url, false, $context);
        $options = array(
            'http' => array(
                'method' => 'GET',
                'header' => generate_request_headers(),
		'content' => $data_string
            )
        );
        $context = stream_context_create($options);
        $add_monitor_response = file_get_contents($url, false, $context);
	echo $add_monitor_response."\n";
        $add_monitor_response = json_decode($add_monitor_response, true);
	print "Got response\n";
	print_r($add_monitor_response);
}


if (isset($_GET['topology'])) {
	$topology = array(
        	'self' => array(),
        	'nodes' => array(),
        	'edges' => array(),
        	'monitoring_rules' => array()
   	 );

    	require_once "db_conf.php";
    	$sql = "SELECT as_name, links_to, self from AS_URLS";
    	$result = $conn->query($sql);

    	while ($row = $result->fetch_assoc()) {
        	if ($row['self'] == 1) {
            		array_push($topology['self'], $row['as_name']);
      		 }
        	array_push($topology['nodes'], $row['as_name']);
      	  	if ($row['links_to'] == "") {
            		continue;
        	}
        	$links_to = explode(",", $row['links_to']);
        	foreach ($links_to as $neighbor_node) {
            		$link = array($row['as_name'], $neighbor_node);
            		array_push($topology['edges'], $link);
        	}
    	}

    	$sql = sprintf("SELECT as_name, match_field, frequency, end_time, monitor_id FROM MONITORING_RULES WHERE end_time >= %d",
        	time());
   	$result = $conn->query($sql);
    	//$topology['monitoring_rules'] = $result->fetch_assoc();
    	while ($row = $result->fetch_assoc()) {
        	array_push($topology['monitoring_rules'],$row);
    	}
    	echo json_encode($topology, true);
}


if (isset($_GET["add_filter_alpha"])){
    	$input = file_get_contents("php://input");
    	$input = json_decode($input, true);
    	require_once "db_conf.php";
    	$sql = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" . $input['as_name'] . "')";
    	$result = $conn->query($sql);
    	while ($row = $result->fetch_assoc()) {
        	$url = $row['server_url'] . "?action=add_filter_all";
        	$options = array(
            		'http' => array(
                	'method' => 'POST',
                	'header' => generate_request_headers()
            		)
        	);
        	$context = stream_context_create($options);
        	$add_monitor_response = file_get_contents($url, false, $context);
        	$add_monitor_response = json_decode($add_monitor_response, true);
    	}
    	require_once "db_conf.php";
    	$sql = "UPDATE MONITORING_RULES SET filter='add_filter' WHERE as_name = '" . $input['as_name'] . "'";
    	$result = $conn->query($sql);
    	$conn->commit();
    	return;
}

//Add filter all used by DDoS with Signature to add filters to all monitoring nodes
if (isset($_GET["add_filter_all"])){
	require_once "db_conf.php";
    	$sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    	$result = $conn->query($sql);
    	$added_filters=array();
    	$success_as_name_id=array();
    	$failed_as_name_id=array();

    	while ($row = $result->fetch_assoc()) {
        	$as_name=$row["as_name"];
        	$monitor_id=$row["monitor_id"];
        	$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
        	$result_1 = $conn->query($sql);
        	$senss_server_url = $result_1->fetch_assoc()["server_url"];
        	$url = $senss_server_url . "?action=add_filter&monitor_id=" . $monitor_id;
        	$options = array(
                	'http' => array(
                	'method' => 'GET',
                	'header' => generate_request_headers()
                	)
        	);
        	$context = stream_context_create($options);
        	$response = file_get_contents($url, false, $context);
		//echo "Response ".$response."\n";
		$response = json_decode($response,true);
        	$httpcode = http_response_code();
        	http_response_code($httpcode);
		if ($response["success"]){
	        	array_push($added_filters,$as_name);
            		array_push($success_as_name_id, array(
                		"as_name" => $response["as_name"],
				"threshold" => $response['threshold'],
				"count" => $response['count'])
            		);
		}
		else{
            		array_push($failed_as_name_id, array(
                		"as_name" => $response["as_name"],
				"error" => $response["error"],
				"threshold" => $response['threshold'],
				"count" => $response['count'],
				"details" => $response["details"])
            		);
		}
    	}
    	foreach ($added_filters as $as_name){
		$sql = "UPDATE MONITORING_RULES SET filter='add_filter' WHERE as_name = '" . $as_name . "'";
    	    	$result = $conn->query($sql);
            	$conn->commit();
	}

    	$responses=array();
    	$responses["sucess"] = $success_as_name_id;
    	$responses["failed"] = $failed_as_name_id;
    	echo json_encode($responses, true);

    	return;
}

//Remove filter all for all the existing filtering rules
if (isset($_GET["remove_filter_all"])){
    	require_once "db_conf.php";
    	$sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    	$result = $conn->query($sql);
    	$removed_filters=array();
    	$success_as_name_id=array();
    	$failed_as_name_id=array();
    	while ($row = $result->fetch_assoc()) {
        	$as_name=$row["as_name"];
        	$monitor_id=$row["monitor_id"];
        	$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
        	$result_1 = $conn->query($sql);
        	$senss_server_url = $result_1->fetch_assoc()["server_url"];
        	$url = $senss_server_url . "?action=remove_filter&monitor_id=" . $monitor_id;
        	$options = array(
                	'http' => array(
                	'method' => 'GET',
                	'header' => generate_request_headers()
                	)
        	);
        	$context = stream_context_create($options);
        	$response = file_get_contents($url, false, $context);
		echo "Response ".$response."\n";
		$response=json_decode($response,true);
        	$httpcode = http_response_code();
       	 	http_response_code($httpcode);

		if ($response["success"]){
	        	array_push($removed_filters,$as_name);
            		array_push($success_as_name_id, array(
                		"as_name" => $response["as_name"])
            		);
		}
		else{
            		array_push($failed_as_name_id, array(
                		"as_name" => $response["as_name"],
				"error" => $response["error"],
				"details" => $response["details"])
            		);
		}

    	}
    	foreach ($removed_filters as $as_name){
		$sql = "UPDATE MONITORING_RULES SET filter='None' WHERE as_name = '" . $as_name . "'";
    	    	$result = $conn->query($sql);
	    	$conn->commit();
	}

    	$responses=array();
    	$responses["sucess"] = $success_as_name_id;
    	$responses["failed"] = $failed_as_name_id;
    	echo json_encode($responses, true);
    	return;
}

//Adds a new monitoring by sending request to the SENSS server
if (isset($_GET['add_monitor'])) {
    	$input = file_get_contents("php://input");
    	$input = json_decode($input, true);
    	$monitoring_end_time = time() + ($input['monitor_frequency'] * $input['monitor_duration']);
    	$success_as_name_id = array();
    	require_once "db_conf.php";

    	$sql_1 = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" . join("','", $input['as_name']) . "')";
    	$result = $conn->query($sql_1);
	$reached=0;
    	while ($row = $result->fetch_assoc()) {
        	$url = $row['server_url'] . "?action=add_monitor";
		$as_name=$row['as_name'];
		if ($input['match']['tcp_src']!=NULL || $input['match']['tcp_dst']!=NULL){
			$input['match']['ip_proto']=6;
		}
		if ($input['match']['udp_src']!=NULL || $input['match']['udp_dst']!=NULL){
			$input['match']['ip_proto']=17;
		}
		$data_to_send = array(
        		'frequency' => $input['monitor_frequency'],
        		'end_time' =>$monitoring_end_time,
        		'match' => array(),
			'priority' => $input['priority']
    		);
    		foreach ($input['match'] as $key => $value) {
        		if ($value != "") {
            			$data_to_send['match'][$key] = $value;
        		}
    		}
		//Note for priority
		$match_to_send=$data_to_send["match"];
    		$data_string = json_encode($data_to_send,true);
        	$options = array(
            		'http' => array(
                	'method' => 'POST',
                	'header' => generate_request_headers(),
                	'content' => $data_string
            		)
        	);
        	$context = stream_context_create($options);
       	 	$add_monitor_response = file_get_contents($url, false, $context);
        	$add_monitor_response = json_decode($add_monitor_response, true);
        	if ($add_monitor_response['success']) {
			$reached=1;
            		array_push($success_as_name_id, array(
                		"as_name" => $row['as_name'],
                		"monitor_id" => $add_monitor_response['monitor_id'],
				"threshold" => $add_monitor_response['threshold'],
				"count" => $add_monitor_response['count'])
            		);
			$monitor_type=$input["monitor_type"];
            		$sql = sprintf("INSERT INTO MONITORING_RULES (as_name, match_field, frequency, end_time, monitor_id, type) VALUES ('%s', '%s', %d, %d, %d, '%s')",
                		$row['as_name'], $data_string, $input['monitor_frequency'], $monitoring_end_time, $add_monitor_response['monitor_id'], $monitor_type);
            		$conn->query($sql);

			$request_type="Monitoring rule";
			$current_time=date("D M d, Y G:i");
			$sql = sprintf("INSERT INTO CLIENT_LOGS (request_type, as_name, match_field, time, monitor_id) VALUES ('%s', '%s', '%s', '%s', %d)",
					$request_type, $as_name, $data_string, $current_time, $add_monitor_response['monitor_id']);
			$conn->query($sql);
        	}
    	}
    	$conn->commit();
	$response = array(
		'success' => true,
		'as_name_id' => $success_as_name_id,
		'match' => $data_to_send,
		'reached' =>$reached,
		'response' => $add_monitor_response['success'],
		'type' => $monitor_type,
		'sql' => $match_to_send
	);

    	http_response_code(200);
    	echo json_encode($response);
    	return;

}

//Gets the monitoring IDs for existing monitoring rules
if (isset($_GET['get_monitor_ids'])) {
    	require_once "db_conf.php";
    	$sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    	$result = $conn->query($sql);
    	$data_to_send=array();
    	while ($row = $result->fetch_assoc()) {
		$as_name=$row["as_name"];
		$monitor_id=$row["monitor_id"];
		$monitor_type=$row["monitor_type"];
		$data_to_send[$as_name]=array();
		$data_to_send[$as_name]["monitor_id"]=$monitor_id;
		$data_to_send[$as_name]["monitor_type"]=$monitor_type;
    	}
    	if (empty($data_to_send)) {
		echo "{}";
		return;
    	}
    	echo json_encode($data_to_send,true);
    	return;
}

//Returns AMON SENSS data
if (isset($_GET['get_amon_data'])) {
    	require_once "db_conf.php";
    	$sql = "SELECT id,as_name,match_field,frequency,monitor_duration from AMON_SENSS WHERE type not like 'done'";
    	$result = $conn->query($sql);
    	$data_to_send=array();
	$counter=0;
    	while ($row = $result->fetch_assoc()) {
		$id=$row["id"];
		$as_name=$row["as_name"];
		$match_field=$row["match_field"];
		$frequency=$row["frequency"];
		$monitor_duration=$row["monitor_duration"];
		$data_to_send[$counter]=array();
		$data_to_send[$counter]["id"]=$id;
		$data_to_send[$counter]["as_name"]=$as_name;
		$data_to_send[$counter]["match_field"]=$match_field;
		$data_to_send[$counter]["frequency"]=$frequency;
		$data_to_send[$counter]["monitor_duration"]=$monitor_duration;
		$counter=$counter+1;
    	}
    	if (empty($data_to_send)) {
		echo "{}";
		return;
    	}
    	echo json_encode($data_to_send,true);
    	return;
}

if (isset($_GET['update_amon'])) {
    	require_once "db_conf.php";
    	$input = file_get_contents("php://input");
    	$input = json_decode($input, true);
	if($input["table"]=="MONITORING_RULES"){
		$sql = sprintf("UPDATE MONITORING_RULES SET message='%s' WHERE monitor_id=%d AND as_name='%s'",$input["message"],(int)$input["id"],$input["as_name"]);
	    	$result = $conn->query($sql);
	}
	if($input["table"]=="AMON_SENSS"){
		$sql = sprintf("UPDATE AMON_SENSS SET type='done' WHERE as_name='%s'",$input["as_name"]);
	    	$result = $conn->query($sql);
	}
	$conn->commit();
	$response=array();
	$response["Done"]=$sql;
    	echo json_encode($response);
    	return;
}



//Removes monitoring rule
if(isset($_GET['remove_monitor'])) {
   	if (!isset($_GET['as_name']) && !isset($_GET['monitor_id'])) {
        	http_response_code(400);
        	return;
    	}
    	$as_name = $_GET['as_name'];
    	$monitor_id = $_GET['monitor_id'];
    	require_once "db_conf.php";

    	$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
    	$result = $conn->query($sql);
    	if ($result->num_rows == 0) {
        	http_response_code(400);
        	return;
    	}
    	$senss_server_url = $result->fetch_assoc()["server_url"];
     	$url = $senss_server_url . "?action=remove_monitor&monitor_id=" . $monitor_id;
    	$options = array(
        	'http' => array(
            	'method' => 'GET',
            	'header' => generate_request_headers()
        	)
    	);

    	$context = stream_context_create($options);

    	$sql = sprintf("DELETE FROM MONITORING_RULES WHERE monitor_id=%d ",$monitor_id);
    	$conn->query($sql);
    	$conn->commit();

    	$response = file_get_contents($url, false, $context);
    	$httpcode = http_response_code();
    	if ($httpcode == 200) {
        	echo $response;
    	}
}

//Gets periodic traffic updates on existing monitoring rules
if (isset($_GET['get_monitor'])) {
	if (!isset($_GET['as_name']) && !isset($_GET['monitor_id'])) {
        	http_response_code(400);
        	return;
    	}
    	$as_name = $_GET['as_name'];
    	$monitor_id = $_GET['monitor_id'];
    	require_once "db_conf.php";

    	$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
    	$result = $conn->query($sql);
    	if ($result->num_rows == 0) {
        	http_response_code(400);
        	return;
    	}
    	$senss_server_url = $result->fetch_assoc()["server_url"];

    	$url = $senss_server_url . "?action=get_monitor&monitor_id=" . $monitor_id;
    	$options = array(
        	'http' => array(
            	'method' => 'GET',
            	'header' => generate_request_headers()
        	)
    	);


    	$context = stream_context_create($options);
    	$response = file_get_contents($url, false, $context);
	$response = json_decode($response, true);
    	//$sql = "SELECT message FROM MONITORING_RULES WHERE monitor_id = '" . $monitor_id . "' AND as_name='".$as_name."'";
    	//$result = $conn->query($sql);
	//$message= $result->fetch_assoc()["message"];

	$response= json_encode($response,true);
    	$httpcode = http_response_code();
    	if ($httpcode == 200) {
        	echo $response;
		$response = json_decode($response, true);
		$request_type="Monitoring stats";
		$current_time=date("D M d, Y G:i");
		$speed=display_threshold($response["data"]["speed"]);
		$sql = sprintf("INSERT INTO CLIENT_LOGS (request_type, as_name, time, monitor_id, speed) VALUES ('%s', '%s', '%s', %d, '%s')",
			$request_type, $as_name, $current_time, $monitor_id, $speed);
		$conn->query($sql);
    	}
}

if(isset($_GET['get_messages'])) {
    	require_once "db_conf.php";
    	$sql = "SELECT as_name,message FROM MONITORING_RULES WHERE type='user'";
    	$result = $conn->query($sql);
	$response=array();
   	while ($row = $result->fetch_assoc()) {
       	 	$as_name=$row["as_name"];
        	$message=$row["message"];
		$response[$as_name]=$message;
   	}
	$response=json_encode($response,true);
	echo $response;

}

//markhere
if(isset($_GET['get_monitor_id_on_filter'])) {
	//$check=array(2048, "57.0.0.1", "52.0.0.2");
        require_once "db_conf.php";
        require_once "constants.php";
    	$input = file_get_contents("php://input");
    	$input = json_decode($input, true);
	$check=$input["matches"];
        $sql = "SELECT as_name,monitor_id,match_field FROM MONITORING_RULES";
        $result = $conn->query($sql);
	$counter=0;
        $all_urls=array();
        while ($row = $result->fetch_assoc()) {
		$counter=$counter+1;
		$all_url[$counter]=$row;
		$as_name=$row["as_name"];
		$monitor_id=$row["monitor_id"];
		$match_field=json_decode($row["match_field"],true);
		$match=$match_field["match"];
		$total=0;
		foreach($match as $key){
			if (in_array($key,$check)){
				$total=$total+1;
			}
		}
		if($total==count($check)){
			$all_urls[$as_name]=$monitor_id;
		}
        }
	echo json_encode($all_urls,true);
}




//Adds traffic filter on existing monitoring rule
if(isset($_GET['add_filter'])) {
	if (!isset($_GET['as_name']) && !isset($_GET['monitor_id'])) {
        	http_response_code(400);
        	return;
    	}
    	$as_name = $_GET['as_name'];
    	$monitor_id = $_GET['monitor_id'];
    	require_once "db_conf.php";
    	$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
    	$result = $conn->query($sql);
    	if ($result->num_rows == 0) {
        	http_response_code(400);
        	return;
    	}
    	$senss_server_url = $result->fetch_assoc()["server_url"];
    	$url = $senss_server_url . "?action=add_filter&monitor_id=" . $monitor_id."&as_name=".$as_name;
    	$options = array(
        	'http' => array(
            	'method' => 'GET',
            	'header' => generate_request_headers()
        	)
    	);
    	$context = stream_context_create($options);
    	$response = file_get_contents($url, false, $context);
    	$response = json_decode($response,true);
    	$httpcode = http_response_code();
    	http_response_code($httpcode);
    	if(!$response["success"]){
    		echo json_encode(array(
        		"as_name" => $response["as_name"],
                	"error" => $response["error"],
			"threshold" => $response["threshold"],
			"count" =>$response["count"],
                	"details" => $response["details"]
        	),true);
		return;
    	}

   	$sql = "UPDATE MONITORING_RULES SET filter='add_filter' WHERE as_name = '" . $as_name . "'";
    	$result = $conn->query($sql);

	$request_type="Add filter";
	$current_time=date("D M d, Y G:i");
	$sql = sprintf("INSERT INTO CLIENT_LOGS (request_type, as_name, time) VALUES ('%s', '%s', '%s')",
			$request_type, $as_name, $current_time);
	$conn->query($sql);

    	$conn->commit();

    	echo json_encode(array(
		"success" => true,
		"as_name" => $response["as_name"],
		"threshold" => $response["threshold"],
		"count" => $response["count"]
	),true);
    	return;
}

//Removes filter
if(isset($_GET['remove_filter'])) {
    	if (!isset($_GET['as_name']) && !isset($_GET['monitor_id'])) {
        	http_response_code(400);
        	return;
    	}
    	$as_name = $_GET['as_name'];
    	$monitor_id = $_GET['monitor_id'];

    	require_once "db_conf.php";

    	$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
    	$result = $conn->query($sql);
    	if ($result->num_rows == 0) {
        	http_response_code(400);
        	return;
    	}
    	$senss_server_url = $result->fetch_assoc()["server_url"];
    	$url = $senss_server_url . "?action=remove_filter&monitor_id=" . $monitor_id."&as_name=".$as_name;
    	$options = array(
        	'http' => array(
            	'method' => 'GET',
            	'header' => generate_request_headers()
        	)
    	);

    	$context = stream_context_create($options);

    	$response = file_get_contents($url, false, $context);
    	$response = json_decode($response,true);
    	$httpcode = http_response_code();
    	http_response_code($httpcode);


    	if(!$response["success"]){
		echo json_encode(array(
                        "as_name" => $response["as_name"],
                        "error" => $response["error"],
                        "details" => $response["details"]
                ),true);
		return;
    	}


    	$sql = "UPDATE MONITORING_RULES SET filter='None' WHERE as_name = '" . $as_name . "'";
    	$result = $conn->query($sql);
    	$conn->commit();

	$request_type="Remove filter";
	$current_time=date("D M d, Y G:i");
	$sql = sprintf("INSERT INTO CLIENT_LOGS (request_type, as_name, time) VALUES ('%s', '%s', '%s')",
			$request_type, $as_name, $current_time);
	$conn->query($sql);


    	echo json_encode(array(
		"success" => true,
		"as_name" => $response["as_name"]
	),true);

    	return;
}

//Sends information to SENSS proxy when SENSS proxy is not reachable
if(isset($_GET['send_proxy_info'])) {
	require_once "db_conf.php";
	require_once "constants.php";
	$to_do=array();
	$fh = fopen('filename.txt','r');
	while ($line = fgets($fh)) {
		$buffer = str_replace(array("\r", "\n"), '', $line);
		array_push($to_do,$buffer);
	}
	fclose($fh);


    	$sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    	$result = $conn->query($sql);
    	$all_urls=array();
   	while ($row = $result->fetch_assoc()) {
		print_r($row)."\n";
		if (in_array($row["as_name"], $to_do)) {
       	 		$as_name=$row["as_name"];
        		$monitor_id=$row["monitor_id"];
			$temp=array($as_name=>$monitor_id);
			array_push($all_urls,$temp);
		}
   	}
	print_r($all_urls);
       /* $data_string = json_encode($all_urls,true);

        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);
        $options = array(
            'http' => array(
                'method' => 'GET',
                'header' => generate_request_headers(),
		'content' => $data_string
            )
        );
	print_r($options);
        $context = stream_context_create($options);
        $add_monitor_response = file_get_contents(PROXY_URL, false, $context);
	echo $add_monitor_response."\n";
        $add_monitor_response = json_decode($add_monitor_response, true);
	print "Got response\n";
	print_r($add_monitor_response);*/
	return;
}



//Sends information to SENSS proxy when SENSS proxy is not reachable
if(isset($_GET['send_proxy_info_amon'])) {
//if (1){
        require_once "db_conf.php";
        require_once "constants.php";
        $input = file_get_contents("php://input");
        $input = json_decode($input, true);
        $data_string = json_encode($input,true);
        $options = array(
                'http' => array(
                'method' => 'GET',
                'header' => generate_request_headers(),
                'content' => $data_string,
                'timeout' =>3)
        );
        $context = stream_context_create($options);
        $add_monitor_response = file_get_contents(PROXY_URL, false, $context);
        $add_monitor_response = json_decode($add_monitor_response, true);
        echo json_encode($add_monitor_response,true);
	return;
}

if(isset($_GET['get_client_logs'])) {
//if(1){
    	if (!isset($_GET['type'])) {
        	http_response_code(400);
        	return;
    	}
	//$type="add_monitor";
	$type=$_GET['type'];
        require_once "db_conf.php";
	switch($type){
		case "add_filter":
	        	$sql="SELECT as_name,time from CLIENT_LOGS where request_type='Add filter'";
			break;
		case "add_monitor":
	        	$sql="SELECT as_name,match_field,time from CLIENT_LOGS where request_type='Monitoring rule'";
			break;
		case "monitor_stats":
	        	$sql="SELECT as_name,match_field,time,speed from CLIENT_LOGS where request_type='Monitoring stats'";
			break;
	}
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
                $return_array=array();
                while ($row = $result->fetch_assoc()) {
                        array_push($return_array,$row);
                }
		echo json_encode(array(
                        "success" => true,
                        "data" => $return_array
                ),true);
		return;
        }
        echo json_encode(array(
                "success" => false,
                "error" => 400
        ),true);
	return;
}


