<?php
function generate_request_headers() {
    $clientcert = file_get_contents('/var/www/html/SENSS/UI_client_server/Client/cert/clientcert.pem');
    $clientcert = base64_encode($clientcert);
    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
}
function makeRandomString($bits = 256) {
    $bytes = ceil($bits / 8);
    $return = '';
    for ($i = 0; $i < $bytes; $i++) {
        $return .= chr(mt_rand(0, 255));
    }
    return $return;
}

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
        $url = "http://56.0.0.1/SENSS/UI_client_server/Proxy/api.php?action=get_nonce";
        $data_string = json_encode($all_urls,true);

        $options = array(
            'http' => array(
                'method' => 'GET',
                'header' => generate_request_headers(),
                'content' => $data_string
            )
        );
        $context = stream_context_create($options);
        $nonce = file_get_contents($url, false, $context);
	echo "Done with the nonce\n";

	$content=array();
	$content["data"]=$all_urls;
	$cnonce = hash('sha512', makeRandomString());

	$hash = hash('sha512', $nonce . $cnonce . json_encode($all_urls,true));
	$content["cnonce"]=$cnonce;
	$content["hash"]=$hash;

        $data_string = json_encode($content,true);
        $url = "http://56.0.0.1/SENSS/UI_client_server/Proxy/api.php?action=proxy_info";
        $options = array(
            'http' => array(
                'method' => 'GET',
                'header' => generate_request_headers(),
                'content' => $data_string
            )
        );
        $context = stream_context_create($options);
        $response= file_get_contents($url, false, $context);
	echo $response;
}
?>
