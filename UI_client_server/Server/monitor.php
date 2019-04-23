
<?php


function add_monitor($client_info, $data)
{
	require_once "db.php";
    	$data = json_decode($data, true);

    	$frequency = (int)$data['frequency'];
    	$end_time = (int)$data['end_time'];
	$priority = (int)$data['priority'];

    	require_once "constants.php";
    	$add_rule_data = array(
        	"dpid" => SWITCH_DPID,
        	"priority" => $priority,
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
            		"error" => $http_code,
	    		"details" => "Problem with RYU controller",
	    		"as_name" => SENSS_AS
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


        $request_type="Add monitor";
        $sql = sprintf("INSERT INTO SERVER_LOGS (as_name, request_type,match_field,end_time) VALUES 
                  ('%s', '%s','%s','%d')", $client_info['as_domain'],$request_type, json_encode($add_rule_data),$end_time);
	        $conn1->query($sql);
        $conn1->commit();

    	return array(
        	"success" => true,
        	"monitor_id" => $id,
		"as_name" => SENSS_AS
    	);
}

function remove_monitor($client_info, $monitor_id)
{
	require_once "db.php";

    	$sql = "UPDATE CLIENT_LOGS SET end_time = " . time() . ",active=0 WHERE as_name = '" . $client_info['as_domain'] . "' 
            AND id = " . (int)$monitor_id . " AND log_type = 'MONITOR'";

    	$conn1->query($sql);
        $conn1->commit();
        $request_type="Remove monitor";
        $sql = sprintf("INSERT INTO SERVER_LOGS (request_type,as_name) VALUES
                  ('%s','%s')", $request_type,$client_info['as_domain']);
        $conn1->query($sql);
        $conn1->commit();
    	require_once "constants.php";
    	return array(
        	"success" => true,
		"as_name" => SENSS_AS
    	);
}


function get_monitor($client_info, $monitor_id)
{
    	require_once "db.php";

    	$sql1 = "SELECT packet_count, byte_count, speed FROM CLIENT_LOGS WHERE as_name = '" . $client_info['as_domain'] . "' 
            AND id = " . (int)$monitor_id . " AND log_type = 'MONITOR' AND end_time >= " . time();

    	$result = $conn1->query($sql1);
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
            		"data" => $result->fetch_assoc(),
	    		"message"=>$sql
        	);
    	}
    	return array(
        	"success" => false,
        	"error" => 400
    	);
}
