<?php


function add_filter($client_info, $monitor_id)
{
    require_once "db.php";

    $sql = sprintf("SELECT match_field FROM CLIENT_LOGS WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR' AND 
            end_time >= %d", $client_info['as_domain'], $monitor_id, time());
    $result = $conn1->query($sql);
    $match_field = $result->fetch_assoc()['match_field'];
    $add_rule_data = json_decode($match_field, true);
    $add_rule_data['action'] = array();

    require_once "constants.php";
    $ch = curl_init(CONTROLLER_BASE_URL . "/stats/flowentry/modify");
    curl_setopt_array($ch, array(
        CURLOPT_POST => TRUE,
        CURLOPT_RETURNTRANSFER => TRUE,
        CURLOPT_HTTPHEADER => array(
            'Content-Type: application/json'
        ),
        CURLOPT_POSTFIELDS => json_encode($add_rule_data)
    ));

    /*curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code != 200) {
        return array(
            "success" => false,
            "error" => $http_code
        );
    }*/

    $sql = sprintf("UPDATE CLIENT_LOGS SET flag = 1 WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR' AND 
            end_time >= %d", $client_info['as_domain'], $monitor_id, time());
    echo $sql;
    $conn1->query($sql);
    $conn1->commit();
}


function remove_filter($client_info, $monitor_id)
{
    require_once "db.php";

    $sql = sprintf("SELECT match_field FROM CLIENT_LOGS WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR'",
        $client_info['as_domain'], $monitor_id);
    $result = $conn1->query($sql);
    $match_field = $result->fetch_assoc()['match_field'];
    $add_rule_data = json_decode($match_field, true);

    require_once "constants.php";
    $ch = curl_init(CONTROLLER_BASE_URL . "/stats/flowentry/delete");
    curl_setopt_array($ch, array(
        CURLOPT_POST => TRUE,
        CURLOPT_RETURNTRANSFER => TRUE,
        CURLOPT_HTTPHEADER => array(
            'Content-Type: application/json'
        ),
        CURLOPT_POSTFIELDS => json_encode($add_rule_data)
    ));

    /*curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code != 200) {
        return array(
            "success" => false,
            "error" => $http_code
        );
    }*/

    $sql = sprintf("UPDATE CLIENT_LOGS SET flag = 0 WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR'",
        $client_info['as_domain'], $monitor_id);
    $conn1->query($sql);
    $conn1->commit();
}
