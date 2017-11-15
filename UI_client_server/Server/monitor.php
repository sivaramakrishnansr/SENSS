<?php


function add_monitor($client_info, $data)
{
    require_once "db.php";

    $data = json_decode($data, true);
    // TODO: Validation code here - check if match nw_dst is contained within client_prefix
    

    $frequency = (int)$data['frequency'];
    $end_time = (int)$data['end_time'];
    $match = json_encode($data['match'], true);

    // TODO: Add rule to controller here

    $sql = sprintf("SELECT * FROM CLIENT_LOGS WHERE as_name = '%s' AND match_field = '%s' AND log_type = 'MONITOR'",
                    $client_info['as_domain'], $match);
    $result = $conn1->query($sql);
    if ($result->num_rows == 1) {
        $id = $result->fetch_assoc()['id'];
        $sql = sprintf("UPDATE CLIENT_LOGS SET frequency = %d, end_time = %d, active = 1 WHERE id = %d",
                        $frequency, $end_time, $id);
        $conn1->query($sql);
        $conn1->commit();
    } else {
        $sql = sprintf("INSERT INTO CLIENT_LOGS (as_name, log_type, match_field, active, frequency, end_time) VALUES 
                  ('%s', 'MONITOR', '%s', 1, %d, %d)", $client_info['as_domain'], $match, $frequency, $end_time);

        $conn1->query($sql);
        $conn1->commit();
    }
    $conn1->close();
}


//The SENSS clients will call this endpoint periodically to receive traffic updates
function get_monitor($client_info, $match_field)
{
    require_once "db.php";

    $sql = "SELECT packet_count, byte_count, speed FROM CLIENT_LOGS WHERE as_name = '" . $client_info['as_domain'] . "' 
            AND match_field = '" . $match_field . "'";

    $result = $conn1->query($sql);
    if ($result->num_rows > 0) {
        return $result->fetch_assoc();
    }
    return array();
}