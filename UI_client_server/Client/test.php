<?php
    $test=array();

    require_once "db_conf.php";
    $sql = sprintf("SELECT as_name, match_field, frequency, end_time, monitor_id FROM MONITORING_RULES WHERE end_time >= %d",
        time());
    $result = $conn->query($sql);
    print_r($result);
    while ($row = $result->fetch_assoc()) {
	print_r($row);
	array_push($test,$row);
    }
    print_r($test);
?>
