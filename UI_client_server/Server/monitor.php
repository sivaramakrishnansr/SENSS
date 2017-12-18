<?php


function add_monitor($client_info, $data)
{
    require_once "db.php";

    $data = json_decode($data, true);
    if (!isset($data['match']['nw_dst'])) {
        return array(
            "success" => false,
            "error" => 401
        );
    }
    require_once "utils.php";
    if (!validate_ip_range($data['match']['nw_dst'], $client_info['client_prefix'])) {
        return array(
            "success" => false,
            "error" => 402
        );
    }

    $frequency = (int)$data['frequency'];
    $end_time = (int)$data['end_time'];

    require_once "constants.php";
    $add_rule_data = array(
        "dpid" => SWITCH_DPID,
        "priority" => 11111,
        "match" => $data['match'],
        "actions" => array(
            array(
                "type" => "OUTPUT",
                "port" => 1
            )
        )
    );
    $add_rule_data['match']['in_port'] = 2;
    $add_rule_data['match']['eth_type'] = 2048;

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
        $sql = sprintf("INSERT INTO CLIENT_LOGS (as_name, log_type, match_field, active, frequency, end_time) VALUES 
                  ('%s', 'MONITOR', '%s', 1, %d, %d)", $client_info['as_domain'], json_encode($add_rule_data),
            $frequency, $end_time);

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

    $sql = "UPDATE CLIENT_LOGS SET end_time = " . time() . " WHERE as_name = '" . $client_info['as_domain'] . "' 
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