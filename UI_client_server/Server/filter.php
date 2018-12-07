<?php

function add_filter_alpha($as_info)
{
	require_once "constants.php";
    	$url=CONTROLLER_BASE_URL . "/stats/flowentry/clear/".SWITCH_DPID;
    	$ch=curl_init($url);
    	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
    	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    	curl_setopt($ch, CURLOPT_HEADER, true);
    	curl_setopt($ch, CURLOPT_NOBODY, true);
    	$output = curl_exec($ch);
    	$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    	curl_close($ch);

    	if ($http_code != 200) {
        	return array(
            		"success" => false,
            		"error" => $http_code,
	    		"as_name" => SENSS_AS,
	    		"details" => "Problem with RYU controller"
        	);
    	}
    	require_once "db.php";
    	$request_type="Add filter all";
    	$sql = sprintf("INSERT INTO SERVER_LOGS (as_name,$request_type) VALUES
                  ('%s','%s')",$as_info['as_domain'],$request_type);
    	$conn1->query($sql);
    	$conn1->commit();

    	return array(
        	"success" => true,
		"as_name" => SENSS_AS,
		"code" => $http_code
    	);
}

function add_filter($as_info, $monitor_id)
{
    	require_once "db.php";

    	$sql = sprintf("SELECT match_field FROM CLIENT_LOGS WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR' AND 
        	    end_time >= %d", $as_info['as_domain'], $monitor_id, time());
    	$result = $conn1->query($sql);
    	$match_field = $result->fetch_assoc()['match_field'];
    	$add_rule_data = json_decode($match_field, true);
    	$add_rule_data['actions'] = array();

    	require_once "constants.php";
    	$ch = curl_init(CONTROLLER_BASE_URL . "/stats/flowentry/modify_strict");
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
            		"error" => $http_code,
	    		"as_name" => SENSS_AS,
	    		"details" => "Problem with RYU controller"
        	);
    	}

    	$sql = sprintf("UPDATE CLIENT_LOGS SET flag = 1 WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR' AND 
        	    end_time >= %d", $as_info['as_domain'], $monitor_id, time());
    	$conn1->query($sql);
    	$conn1->commit();

        $request_type="Add filter";
        $sql = sprintf("INSERT INTO SERVER_LOGS (as_name,request_type,match_field) VALUES
                  ('%s','%s','%s')",$as_info['as_domain'],$request_type,json_encode($add_rule_data));
        $conn1->query($sql);
        $conn1->commit();

    	return array(
        	"success" => true,
		"as_name" => SENSS_AS,
		"code" => $http_code
    	);
}


function remove_filter($as_info, $monitor_id)
{
    	require_once "db.php";

    	$sql = sprintf("SELECT match_field FROM CLIENT_LOGS WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR'",
        	$as_info['as_domain'], $monitor_id);
    	$result = $conn1->query($sql);
    	$match_field = $result->fetch_assoc()['match_field'];
    	$add_rule_data = json_decode($match_field, true);

    	require_once "constants.php";
    	$ch = curl_init(CONTROLLER_BASE_URL . "/stats/flowentry/modify_strict");
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
            		"error" => $http_code,
	    		"as_name" => SENSS_AS,
	    		"details" => "Problem with RYU controller"
        	);
    	}

    	$sql = sprintf("UPDATE CLIENT_LOGS SET flag = 0 WHERE as_name = '%s' AND id = %d AND log_type = 'MONITOR'",
        	$as_info['as_domain'], $monitor_id);
    	$conn1->query($sql);
    	$conn1->commit();

        $request_type="Remove filter";
        $sql = sprintf("INSERT INTO SERVER_LOGS (request_type,as_name,match_field) VALUES
                  ('%s','%s','%s')", $request_type,$as_info['as_domain'],json_encode($add_rule_data));
        $conn1->query($sql);
        $conn1->commit();

    	return array(
        	"success" => true,
		"code" => $http_code,
		"as_name" => SENSS_AS
    	);
}
