<?php


function add_monitor($client_info, $data)
//if(1)
{
    require_once "db.php";


    //Blocked for testing purpose
    $data = json_decode($data, true);

    /*if (!isset($data['match']['nw_dst'])) {
        return array(
            "success" => false,
            "error" => 401
        );
    }*/
    //require_once "utils.php";
    //if (!validate_ip_range($data['match']['nw_dst'], $client_info['client_prefix'])) {
    //    return array(
    //        "success" => false,
    //        "error" => 402
    //    );
    //}

    //Blocked for testing purpose
    $frequency = (int)$data['frequency'];
    $end_time = (int)$data['end_time'];


    require_once "constants.php";
    $add_rule_data = array(
        "dpid" => SWITCH_DPID,
        "priority" => 11111,
        //Blocked for testing purpose
        "match" => $data['match'],
        "actions" => array(
            array(
                "type" => "OUTPUT",
                "port" => 1
            ),
	    array(
		"type" => "OUTPUT",
		"port" =>2
	    )
        )
    );
    //$add_rule_data['match']['in_port'] = 2;
    $add_rule_data["match"]["eth_type"] = 2048;

    $ch = curl_init(CONTROLLER_BASE_URL . "/stats/flowentry/add");
    curl_setopt_array($ch, array(
        CURLOPT_POST => TRUE,
        CURLOPT_RETURNTRANSFER => TRUE,
        CURLOPT_HTTPHEADER => array(
            'Content-Type: application/json'
        ),
        CURLOPT_POSTFIELDS => json_encode($add_rule_data, JSON_UNESCAPED_SLASHES)
    ));

    curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code != 200) {
        return array(
            "success" => false,
            "error" => $http_code
        );
    }

    $sql = sprintf("SELECT * FROM CLIENT_LOGS WHERE as_name = '%s' AND match_field = '%s' AND log_type = 'MONITOR'",
        $client_info['as_domain'], json_encode($add_rule_data));


    $result = $conn1->query($sql);
    $id = 0;
    if ($result->num_rows == 1) {
        $id = $result->fetch_assoc()['id'];
        $sql = sprintf("UPDATE CLIENT_LOGS SET frequency = %d, end_time = %d, active = 1 WHERE id = %d",
            $frequency, $end_time, $id);
        $conn1->query($sql);
        $conn1->commit();
    } else {
        $sql = sprintf("INSERT INTO CLIENT_LOGS (as_name, log_type, match_field, active, frequency, end_time,packet_count,byte_count,speed) VALUES 
                  ('%s', 'MONITOR', '%s', 1, %d, %d,%d,%d,%d)", $client_info['as_domain'], json_encode($add_rule_data),
            $frequency, $end_time,0,0,0);

        $conn1->query($sql);
        $conn1->commit();
        $sql = sprintf("SELECT id FROM CLIENT_LOGS WHERE as_name = '%s' AND match_field = '%s' AND log_type = 'MONITOR'",
            $client_info['as_domain'], json_encode($add_rule_data));
        $result = $conn1->query($sql);
        if ($result->num_rows == 1) {
            $id = $result->fetch_assoc()['id'];
        }
    }
    $conn1->close();

    return array(
        "success" => true,
        "monitor_id" => $id
    );
}

function remove_monitor($client_info, $monitor_id)
{
    require_once "db.php";

    $sql = "UPDATE CLIENT_LOGS SET end_time = " . time() . ",active=0 WHERE as_name = '" . $client_info['as_domain'] . "' 
            AND id = " . (int)$monitor_id . " AND log_type = 'MONITOR'";

    $conn1->query($sql);
}

//The SENSS clients will call this endpoint periodically to receive traffic updates
function get_monitor($client_info, $monitor_id)
{
    require_once "db.php";

    $sql = "SELECT packet_count, byte_count, speed FROM CLIENT_LOGS WHERE as_name = '" . $client_info['as_domain'] . "' 
            AND id = " . (int)$monitor_id . " AND log_type = 'MONITOR' AND end_time >= " . time();

    $result = $conn1->query($sql);
    if ($result->num_rows > 0) {
    	    $sql = "SELECT match_field,packet_count, byte_count, speed FROM CLIENT_LOGS WHERE as_name = '" . $client_info['as_domain'] . "' 
        	    AND id = " . (int)$monitor_id . " AND log_type = 'MONITOR' AND end_time >= " . time();
	    $log_result = $conn1->query($sql);
	    $row=$log_result->fetch_assoc();
	    $match=$row["match_field"];
	    $packet_count=$row["packet_count"];
	    $byte_count=$row["byte_count"];
	    $speed=$row["speed"];
	    $request_type="Get flow stats";
        $sql = sprintf("INSERT INTO SERVER_LOGS (as_name, request_type,match_field,packet_count,byte_count,speed) VALUES 
                  ('%s', '%s','%s', %d,%d,%d)", $client_info['as_domain'],$request_type, json_encode($match),$packet_count,$byte_count,$speed);
        $conn1->query($sql);
        $conn1->commit();

        return array(
            "success" => true,
            "data" => $result->fetch_assoc()
        );
    }
    return array(
        "success" => false,
        "error" => 400
    );
}
