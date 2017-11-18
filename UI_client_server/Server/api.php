<?php

if (!isset($_GET['action'])) {
    http_response_code(400);
    return;
}
/* Authenticate Client */
require_once "client_auth.php";
$client_info = client_auth(apache_request_headers());
if (!$client_info) {
    http_response_code(400);
    return;
}

$action = $_GET['action'];

switch ($action) {
    case "add_filter":
        require_once "filter.php";
        if (!isset($_GET['monitor_id'])) {
            echo json_encode(array(
                    "success" => false,
                    "error" => 400
                )
            );
            return;
        }
        add_filter($client_info, (int)$_GET['monitor_id']);
        http_response_code(200);
        break;

    case "remove_filter":
        require_once "filter.php";
        if (!isset($_GET['monitor_id'])) {
            echo json_encode(array(
                    "success" => false,
                    "error" => 400
                )
            );
            return;
        }
        remove_filter($client_info, (int)$_GET['monitor_id']);
        http_response_code(200);
        break;

    case "add_monitor":
        require_once "monitor.php";
        $response = add_monitor($client_info, file_get_contents("php://input"));
        http_response_code(200);
        echo json_encode($response, true);
        break;

    case "remove_monitor":
        require_once "monitor.php";
        if (!isset($_GET['monitor_id'])) {
            echo json_encode(array(
                    "success" => false,
                    "error" => 400
                )
            );
            return;
        }
        remove_monitor($client_info, (int)$_GET['monitor_id']);
        http_response_code(200);
        break;

    case "get_monitor":
        require_once "monitor.php";
        if (!isset($_GET['monitor_id'])) {
            echo json_encode(array(
                    "success" => false,
                    "error" => 400
                )
            );
            return;
        }
        $data = get_monitor($client_info, (int)$_GET['monitor_id']);
        http_response_code(200);
        echo json_encode($data, true);
        return;

    default:
        http_response_code(400);
        return;
}