<?php

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

    $sql = sprintf("SELECT as_name, match_field, frequency, end_time FROM MONITORING_RULES WHERE end_time >= %d",
        time());
    $result = $conn->query($sql);
    $topology['monitoring_rules'] = $result->fetch_all();
    /*
    $topology = array(
        'self' => 'Porto',
        'nodes' => array(
            'Rennes', 'Eindhoven', 'Paris', 'Madrid', 'Faro', 'Barcelona', 'London', 'Berlin', 'New York', 'Manchester', 'Munich', 'Lisbon', 'Amsterdam', 'Frankfurt'
        ),
        'edges' => array(
            array("Porto", "Lisbon"),
            array("Rennes", "Paris"),
            array("Eindhoven", "Amsterdam"),
            array("Paris", "Frankfurt"),
            array("Paris", "London"),
            array("Paris", "Barcelona"),
            array("Madrid", "Barcelona"),
            array("Madrid", "Lisbon"),
            array("Faro", "Lisbon"),
            array("London", "New York"),
            array("London", "Manchester"),
            array("London", "Lisbon"),
            array("London", "Amsterdam"),
            array("London", "Frankfurt"),
            array("Berlin", "Frankfurt"),
            array("Berlin", "Munich"),
            array("Munich", "Frankfurt"),
            array("Amsterdam", "Frankfurt")

        )
    );
    */

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

    $success_as_name = array();

    require_once "db_conf.php";
    $sql = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" . join("','", $input['as_name']) . "')";
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
//        $url = $row['server_url'] . "/api.php?action=add_monitor";
        $url = "http://localhost/SENSS_proxy/html/server/api.php?action=add_monitor";
        $options = array(
            'http' => array(
                'method' => 'POST',
                'header' => generate_request_headers(),
                'content' => $data_string
            )
        );

        $context = stream_context_create($options);

        echo file_get_contents($url, false, $context);
        $httpcode = http_response_code();
        if ($httpcode == 200) {
            array_push($success_as_name, $row['as_name']);
        }

        $sql = sprintf("INSERT INTO MONITORING_RULES (as_name, match_field, frequency, end_time) VALUES ('%s', '%s', %d, %d)",
            $row['as_name'], $data_string, $input['monitor_frequency'], $monitoring_end_time);
        $conn->query($sql);
    }
    $conn->commit();
    $response = array(
        'as_name' => $success_as_name,
        'match' => $data_to_send
    );

    echo json_encode($response, true);
}


if (isset($_GET['get_monitor'])) {
    if (!isset($_GET['as_name'])) {
        http_response_code(400);
        return;
    }
    $as_name = $_GET['as_name'];

    $input = file_get_contents("php://input");

    require_once "db_conf.php";

    $sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
    $result = $conn->query($sql);
    if ($result->num_rows == 0) {
        http_response_code(400);
        return;
    }
    $senss_server_url = $result->fetch_all()[0][0];

//    $url = $senss_server_url . "/api.php?action=get_monitor";
    $url = "http://localhost/SENSS_proxy/html/server/api.php?action=get_monitor";
    $options = array(
        'http' => array(
            'method' => 'POST',
            'header' => generate_request_headers(),
            'content' => $input
        )
    );

    $context = stream_context_create($options);

    $response = file_get_contents($url, false, $context);
    $httpcode = http_response_code();
    if ($httpcode == 200) {
        echo $response;
    }
}