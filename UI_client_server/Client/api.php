<?php

$server_base_url = "http://localhost/SENSS/UI_client_server/Server/api.php";

function generate_request_headers() {
    $clientcert = file_get_contents('cert/node1cert.pem');
    $clientcert = base64_encode($clientcert);

    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
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
    $topology['monitoring_rules'] = $result->fetch_all();

    echo json_encode($topology, true);
}

if (isset($_GET['add_monitor'])) {
    $input = file_get_contents("php://input");
    $input = json_decode($input, true);

    $monitoring_end_time = time() + ($input['monitor_frequency'] * $input['monitor_duration']);

    $data_to_send = array(
        'frequency' => $input['monitor_frequency'],
        'end_time' => $monitoring_end_time,
        'match' => array()
    );
    foreach ($input['match'] as $key => $value) {
        if ($value != "") {
            $data_to_send['match'][$key] = $value;
        }
    }
    $data_string = json_encode($data_to_send);

    $success_as_name_id = array();

    require_once "db_conf.php";
    $sql = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" . join("','", $input['as_name']) . "')";
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
//        $url = $row['server_url'] . "/api.php?action=add_monitor";
        $url = $server_base_url . "?action=add_monitor";
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

    }
    $conn->commit();
    $response = array(
        'as_name_id' => $success_as_name_id,
        'match' => $data_to_send
    );

    echo json_encode($response, true);
}

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
    $senss_server_url = $result->fetch_all()[0][0];

//    $url = $senss_server_url . "/api.php?action=get_monitor&monitor_id=" . $monitor_id;
    $url = $server_base_url . "?action=remove_monitor&monitor_id=" . $monitor_id;
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
    $senss_server_url = $result->fetch_all()[0][0];

//    $url = $senss_server_url . "/api.php?action=get_monitor&monitor_id=" . $monitor_id;
    $url = $server_base_url . "?action=get_monitor&monitor_id=" . $monitor_id;
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