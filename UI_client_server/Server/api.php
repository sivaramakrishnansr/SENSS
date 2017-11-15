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
        require_once "add_filter.php";
        if (!add_filter(file_get_contents("php://input"))) {
            http_response_code(400);
            return;
        }
        break;

    case "remove_filter":
        break;

    case "add_monitor":
        require_once "monitor.php";
        add_monitor($client_info, file_get_contents("php://input"));
        http_response_code(200);
        break;

    case "get_monitor":
        require_once "monitor.php";
        $data = get_monitor($client_info, file_get_contents("php://input"));
        http_response_code(200);
        echo json_encode($data, true);
        return;

    default:
        http_response_code(400);
        return;
}