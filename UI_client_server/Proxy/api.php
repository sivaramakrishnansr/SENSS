<?php

if (!isset($_GET['action'])) {
    http_response_code(400);
    return;
}
/* Authenticate Client */
//require_once "client_auth.php";
//$client_info = client_auth(apache_request_headers());
//if (!$client_info) {
//    http_response_code(400);
//    return;/
//}

$action = $_GET['action'];
switch ($action) {
    case "add_monitor":
        require_once "db_conf.php";
	$data=file_get_contents("php://input");
	$data=json_decode($data,true);
	$sql = sprintf("INSERT INTO MONITORING_RULES (as_name, match_field, frequency, end_time, monitor_id) VALUES ('%s', '%s', %d, %d, %d)",
                $data['as_name'], $data['match_field'], $data['frequency'], $data['end_time'], $data['monitor_id']);
        $conn->query($sql);
        http_response_code(200);
        break;
}
