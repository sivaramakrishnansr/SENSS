<?php
function generate_request_headers() {
    $clientcert = file_get_contents('/var/www/html/SENSS/UI_client_server/Client/cert/clientcert.pem');
    $clientcert = base64_encode($clientcert);
    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
}

        require_once "db_conf.php";
        require_once "constants.php";
        $to_do=array();
        $fh = fopen('alerts.txt','r');
        while ($line = fgets($fh)) {
                $buffer = str_replace(array("\r", "\n"), '', $line);
                array_push($to_do,$buffer);
        }
        fclose($fh);


        $sql = "SELECT as_name,monitor_id,match_field FROM MONITORING_RULES";
        $result = $conn->query($sql);
        $all_urls=array();
        while ($row = $result->fetch_assoc()) {
                        $as_name=$row["as_name"];
                        $monitor_id=$row["monitor_id"];
                        foreach($to_do as $src_ip) {
                                echo $src_ip." ".$row["match_field"]."\n";
                                if (strpos($row["match_field"], $src_ip) !== false)
                                {
                                        $temp=array($as_name=>$monitor_id);
                                        array_push($all_urls,$temp);
                                }
                        }
        }
        print_r($all_urls);
        echo "\n";
        print_r($to_do);
        print_r($all_urls);
        $data_string = json_encode($all_urls,true);

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
        print_r($add_monitor_response);
        return;
?>
