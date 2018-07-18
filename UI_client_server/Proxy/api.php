<!--
#
# Copyright (C) 2018 University of Southern California.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
-->

<?php
$action = $_GET['action'];
function generate_request_headers() {
    ///var/www/html/SENSS/UI_client_server/Client/cert
    $clientcert = file_get_contents('/var/www/html/SENSS/UI_client_server/Client/cert/clientcert.pem');
    $clientcert = base64_encode($clientcert);
    return array(
        "Content-Type: application/json",
        "X-Client-Cert: " . $clientcert
    );
}
//$action="proxy_info";
switch ($action) {
    case "proxy_info":
        http_response_code(200);
	$content=json_decode(file_get_contents("php://input"),true);
	//$content=array(
	//	"hpc054"=>1
	//);
	$return_array=array();
	foreach($content as $monitoring_item){
		foreach($monitoring_item as $as_name=>$monitor_id){
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
			echo $url."\n";
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
                		"count" => $response["count"]
        		),true);
		}
	}
}
?>
