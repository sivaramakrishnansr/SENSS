<?php

//$server_base_url = "http://hpc057/SENSS/UI_client_server/Server/api.php";
$proxy_base_url = "http://hpc056/SENSS/UI_client_server/Proxy/api.php";

function generate_request_headers() {
    ///var/www/html/SENSS/UI_client_server/Client/cert
    $clientcert = file_get_contents('/var/www/html/SENSS/UI_client_server/Client/cert/clientcert.pem');
    $clientcert = base64_encode($clientcert);
    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
}


if(isset($_GET['check'])){
    $url = "http://hpc052/SENSS/UI_client_server/Server/api.php?action=check";
        $options = array(
            'http' => array(
                'method' => 'POST',
                'header' => generate_request_headers()
            )
        );
	//print_r($options);
        $context = stream_context_create($options);
        $add_monitor_response = file_get_contents($url, false, $context);
        $add_monitor_response = json_decode($add_monitor_response, true);
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
//if(1){
    $input = file_get_contents("php://input");
    $input = json_decode($input, true);
    //$input=array("as_name"=>"hpc052");
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


//I would create a wrapper function which calls all of them individually
if (isset($_GET["add_filter_all"])){
    require_once "db_conf.php";
    $sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    $result = $conn->query($sql);
    $added_filters=array();
    while ($row = $result->fetch_assoc()) {
        $as_name=$row["as_name"];
        $monitor_id=$row["monitor_id"];
        array_push($added_filters,$as_name);
        $sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
        $result_1 = $conn->query($sql);
        $senss_server_url = $result_1->fetch_assoc()["server_url"];
        echo $as_name." ".$monitor_id." ".$senss_server_url."\n";
        $url = $senss_server_url . "?action=add_filter&monitor_id=" . $monitor_id;
        $options = array(
                'http' => array(
                'method' => 'GET',
                'header' => generate_request_headers()
                )
        );
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);
        $httpcode = http_response_code();
        http_response_code($httpcode);
    }
    foreach ($added_filters as $as_name){
	    $sql = "UPDATE MONITORING_RULES SET filter='add_filter' WHERE as_name = '" . $as_name . "'";
    	    $result = $conn->query($sql);
            $conn->commit();
	}
    return;
}
//Remove filter all
if (isset($_GET["remove_filter_all"])){
    require_once "db_conf.php";
    $sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    $result = $conn->query($sql);
    $removed_filters=array();
    while ($row = $result->fetch_assoc()) {
        $as_name=$row["as_name"];
        $monitor_id=$row["monitor_id"];
	array_push($removed_filters,$as_name);
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
        $httpcode = http_response_code();
        http_response_code($httpcode);
    }
    foreach ($removed_filters as $as_name){
	    $sql = "UPDATE MONITORING_RULES SET filter='None' WHERE as_name = '" . $as_name . "'";
    	    $result = $conn->query($sql);
	}
    $conn->commit();
    return;
}

if (isset($_GET['add_monitor'])) {
//if (1){
    $input = file_get_contents("php://input");
    $input = json_decode($input, true);
    /*$input=array(
      "monitor_frequency"=>500,
      "monitor_duration"=>1,
      "match"=>array(
              "nw_dst"=>"10.0.0.1",
              "nw_src"=>"10.0.0.2"
     ),
      "as_name"=>"hpc057"
    );*/

    $monitoring_end_time = time() + ($input['monitor_frequency'] * $input['monitor_duration']);


    $success_as_name_id = array();

    require_once "db_conf.php";

    $sql = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" . join("','", $input['as_name']) . "')";
    //$sql = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" .$input['as_name'] . "')";
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
        $url = $row['server_url'] . "?action=add_monitor";
        //$url = "http://hpc056:80/SENSS/UI_client_server/Server/api.php?action=add_monitor";
        //$url = $server_base_url . "?action=add_monitor";
	$temp=$row['as_name'];
	$as_name_temp=str_replace("hpc0","",$temp);
	$input['match']['nw_src']=$as_name_temp.".0.0.1";
	$input['match']['nw_proto']=17;
	$data_to_send = array(
        	'frequency' => $input['monitor_frequency'],
        	'end_time' =>$monitoring_end_time,
        	'match' => array()
    	);
    	foreach ($input['match'] as $key => $value) {
        	if ($value != "") {
            	$data_to_send['match'][$key] = $value;
        	}
    	}
    	$data_string = json_encode($data_to_send);

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
            array_push($success_as_name_id, array(
                "as_name" => $row['as_name'],
                "monitor_id" => $add_monitor_response['monitor_id'])
            );
            $sql = sprintf("INSERT INTO MONITORING_RULES (as_name, match_field, frequency, end_time, monitor_id) VALUES ('%s', '%s', %d, %d, %d)",
                $row['as_name'], $data_string, $input['monitor_frequency'], $monitoring_end_time, $add_monitor_response['monitor_id']);
            $conn->query($sql);
        }

	//Sending proxy data
	$proxy_data=array(
		'as_name'=>$row['as_name'],
		'match_field'=>$data_string,
		'frequency'=>$input['monitor_frequency'],
		'end_time'=>$monitoring_end_time,
		'monitor_id'=>$add_monitor_response['monitor_id']
	);
    	$data_string = json_encode($proxy_data);
        $options = array(
            'http' => array(
                'method' => 'POST',
                'header' => generate_request_headers(),
                'content' => $data_string
            )
        );
        $url = $proxy_base_url . "?action=add_monitor";
        $context = stream_context_create($options);
        $add_monitor_response = file_get_contents($url, false, $context);

    }
    $conn->commit();
    $response = array(
        'as_name_id' => $success_as_name_id,
        'match' => $data_to_send
    );

    echo json_encode($response, true);

}

//plsmark
if (isset($_GET['get_monitor_ids'])) {
//if(1){
    require_once "db_conf.php";
    $sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    $result = $conn->query($sql);
    $data_to_send=array();
    while ($row = $result->fetch_assoc()) {
	$as_name=$row["as_name"];
	$monitor_id=$row["monitor_id"];
	$data_to_send[$as_name]=$monitor_id;
    }
    if (empty($data_to_send)) {
	echo "{}";
	return;
    }
    echo json_encode($data_to_send,true);
    return;
}

if (isset($_GET['get_monitor_status'])) {
    $as_name=$_GET['as_name'];
    require_once "db_conf.php";
    $sql = "SELECT filter FROM MONITORING_RULES WHERE as_name ='". $as_name . "'";
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
	$filter_tag=$row["filter"];
    }
    echo $filter_tag;
}


//Remove monitor removes from the database as well
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
    //$url = $server_base_url . "?action=remove_monitor&monitor_id=" . $monitor_id;
    $options = array(
        'http' => array(
            'method' => 'GET',
            'header' => generate_request_headers()
        )
    );

    $context = stream_context_create($options);

    //$sql = sprintf("DELETE FROM MONITORING_RULES WHERE id = %d", $monitor_id);
    $sql = sprintf("DELETE FROM MONITORING_RULES WHERE monitor_id=%d ",$monitor_id);
    $conn->query($sql);
    $conn->commit();

    $response = file_get_contents($url, false, $context);
    $httpcode = http_response_code();
    if ($httpcode == 200) {
        echo $response;
    }
}

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
    //$url = $server_base_url . "?action=get_monitor&monitor_id=" . $monitor_id;
    $options = array(
        'http' => array(
            'method' => 'GET',
            'header' => generate_request_headers()
        )
    );

    $context = stream_context_create($options);


    $response = file_get_contents($url, false, $context);
    $httpcode = http_response_code();
    if ($httpcode == 200) {
        echo $response;
    }
}


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
    $httpcode = http_response_code();
    http_response_code($httpcode);

    $sql = "UPDATE MONITORING_RULES SET filter='add_filter' WHERE as_name = '" . $as_name . "'";
    $result = $conn->query($sql);
    $conn->commit();


    return;
}

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
    $httpcode = http_response_code();
    http_response_code($httpcode);

    $sql = "UPDATE MONITORING_RULES SET filter='None' WHERE as_name = '" . $as_name . "'";
    $result = $conn->query($sql);
    $conn->commit();

    return;
}

if(isset($_GET['send_proxy_info'])) {
//if(1){
	//$command = escapeshellcmd('sudo ./client.py');
	echo shell_exec("./client.py");
	return;
}
