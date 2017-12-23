<?php
    require_once "db.php";
    $monitor_id=30;
    $sql = "SELECT packet_count, byte_count, speed FROM CLIENT_LOGS WHERE " . "
             id = " . (int)$monitor_id . " AND log_type = 'MONITOR' AND end_time >= " . time();

    echo $sql."\n";
    $result = $conn1->query($sql);
    print_r($result);
    if ($result->num_rows > 0) {
            $sql = "SELECT match_field,packet_count, byte_count, speed FROM CLIENT_LOGS WHERE as_name = '" . $client_info['as_domain'] . "'
                    AND id = " . (int)$monitor_id . " AND log_type = 'MONITOR' AND end_time >= " . time();
            $log_result = $conn1->query($sql);
            $row=$log_result->fetch_assoc();
	    print_r($row);
            $match=$row["match_field"];
            $packet_count=$row["packet_count"];
            $byte_count=$row["byte_count"];
            $speed=$row["speed"];

        $sql = sprintf("INSERT INTO SERVER_LOGS (match_field,packet_count,byte_count,speed) VALUES
                  ('%s', %d,%d,%d)" ,json_encode($match),$packet_count,$byte_count,$speed);
	echo $sql."\n";
        $conn1->query($sql);
        $conn1->commit();
 }
?>
