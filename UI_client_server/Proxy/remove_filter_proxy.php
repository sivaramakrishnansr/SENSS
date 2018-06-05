<?php
function generate_request_headers() {
    $clientcert = file_get_contents('/var/www/html/SENSS/UI_client_server/Client/cert/node1cert.pem');
    $clientcert = base64_encode($clientcert);
    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
}

    require_once "db_conf.php";
    $sql = "SELECT as_name,monitor_id FROM MONITORING_RULES";
    $result = $conn->query($sql);
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
        $httpcode = http_response_code();
        http_response_code($httpcode);
    }
?>
