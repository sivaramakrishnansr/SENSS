<?php

//The SENSS clients will call this endpoint periodically to receive traffic updates
function get_server_logs()
{
    require_once "db.php";
    $sql ="SELECT * FROM SERVER_LOGS";
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
