<?php

//The SENSS clients will call this endpoint periodically to receive traffic updates
function get_server_logs()
{
    require_once "db.php";
    //$sql ="SELECT * FROM SERVER_LOGS";
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

function get_count()
{
    require_once "db.php";
    $sql="SELECT as_name,request_type,COUNT(request_type) AS count_request_type,end_time from SERVER_LOGS WHERE  request_type='Add filter' OR (request_type='Add monitor' AND ".time()."<end_time) OR request_type='Remove filter' GROUP BY request_type";
    echo $sql."\n";
    $result = $conn1->query($sql);
    $add_filter=0;
    $remove_filter=0;
    $add_monitor=0;
    if ($result->num_rows > 0) {
	$return_array=array();
	while ($row = $result->fetch_assoc()) {
		if ($row["request_type"]=="Add filter"){
			$add_filter=$row["count_request_type"];
		}
		if ($row["request_type"]=="Remove filter"){
			$remove_filter=$row["count_request_type"];
		}
		if ($row["request_type"]=="Add monitor"){
			$end_time=(int)$row["end_time"];
			echo $end_time."\n";
			echo time()."\n";
			if (time()<$end_time){
				$add_monitor=$row["count_request_type"];
			}
		}
	}
    }
    $total=$add_filter-$remove_filter+$add_monitor;
    return array("total"=>$total);
}
?>
