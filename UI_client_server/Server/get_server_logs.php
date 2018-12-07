
<?php

function get_server_logs()
{
    	require_once "db.php";
    	$sql="SELECT as_name,request_type,COUNT(request_type) AS count_request_type,match_field,AVG(packet_count) AS avg_packet_count,AVG(speed) AS avg_speed from SERVER_LOGS GROUP BY request_type";
    	$result = $conn1->query($sql);
    	if ($result->num_rows > 0) {
		$return_array=array();
		while ($row = $result->fetch_assoc()) {
			array_push($return_array,$row);
		}
        	return array(
            		"success" => true,
            		"data" => $return_array
        	);
    	}
    	return array(
        	"success" => false,
        	"error" => 400
    	);
}
?>
