<?php
function generate_request_headers() {
    ///var/www/html/SENSS/UI_client_server/Client/cert
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

require_once "client_auth.php";
//print_r(apache_request_headers());
$client_info = client_auth(apache_request_headers());
if (!$client_info) {
        http_response_code(400);
        return;
}


$action = $_GET['action'];
//$action="get_nonce";
switch ($action) {
    case "get_nonce":
	$id = $_SERVER['HTTP_CLIENT_IP'] ? $_SERVER['HTTP_CLIENT_IP'] : ($_SERVER['HTTP_X_FORWARDED_FOR'] ? $_SERVER['HTTP_X_FORWARDED_FOR'] : $_SERVER['REMOTE_ADDR']);
	$nonce = hash('sha512', makeRandomString());
	$servername = "localhost";
	$username = "root";
	$password = "usc558l";
	$dbname = "SENSS_PROXY";
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	}
	$sql = "SELECT id FROM NONCES WHERE ip = '" . $id . "'";
	$result = $conn->query($sql);
	if ($result->num_rows == 0) {
		$sql = sprintf("INSERT INTO NONCES (ip,nonce) VALUES ('%s','%s')",$id,$nonce);
	        $conn->query($sql);
        	$conn->commit();
	}
	else{
		$key=$result->fetch_assoc()["id"];
		$sql = sprintf("UPDATE NONCES SET nonce='%s' WHERE id='%s'",$nonce,$key);
	        $conn->query($sql);
        	$conn->commit();
	}
	echo $nonce;
	return;

    case "proxy_info":
	$id = $_SERVER['HTTP_CLIENT_IP'] ? $_SERVER['HTTP_CLIENT_IP'] : ($_SERVER['HTTP_X_FORWARDED_FOR'] ? $_SERVER['HTTP_X_FORWARDED_FOR'] : $_SERVER['REMOTE_ADDR']);
	$servername = "localhost";
	$username = "root";
	$password = "usc558l";
	$dbname = "SENSS_PROXY";
	$conn = new mysqli($servername, $username, $password, $dbname);
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	}
	$sql = "SELECT nonce FROM NONCES WHERE ip = '" . $id . "'";
	$result = $conn->query($sql);
	$nonce=$result->fetch_assoc()["nonce"];
	$sql = sprintf("DELETE FROM NONCES WHERE nonce='%s'",$nonce);
	$conn->query($sql);
	$conn->commit();
	$content=json_decode(file_get_contents("php://input"),true);
	$cnonce=$content["cnonce"];
	$hash=$content["hash"];
	$content=$content["data"];
	$testHash = hash('sha512',$nonce . $cnonce . json_encode($content,true));
	echo "\n";
	echo $hash."\n";
	echo $testHash."\n";
	if ($testHash==$hash){
		echo "Verification complete";
		return;
	}
	return;
        http_response_code(200);
	$content=json_decode(file_get_contents("php://input"),true);
	//$content=array(
	//	"hpc052"=>1
	//);
	$return_array=array();
	$content=$content["data"];
	foreach($content as $as_name=>$monitor_id){
			$monitor_id=(string) $monitor_id;
			require_once "db_conf.php";
    			$sql = "SELECT server_url FROM AS_URLS WHERE as_name = '" . $as_name . "'";
    			$result = $conn->query($sql);
    			if ($result->num_rows == 0) {
       	 			http_response_code(400);
    		    		return;
    			}
    			$senss_server_url = $result->fetch_assoc()["server_url"];
			array_push($return_array,$senss_server_url);
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
    			echo json_encode(array(
                		"success" => true,
                		"as_name" => $response["as_name"],
                		"threshold" => $response["threshold"],
                		"count" => $response["count"],
				"url" => $url
        		),true);
			return;
	}
}
?>
