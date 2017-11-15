<?php

/**
* This script runs as a SENSS Server. This is to be deployed on all ASes.
* The API's here will be called by the SENSS client script add_filter.php
*/

$controller_base_url = "http://127.0.0.1:8000"; // CONTROLLER URL HARDCODED

function validate_request($request_data) {

	/* Validation code goes here */
	return true;
}

function send_request($request_data) {
	global $controller_base_url;
    $get_dpid_url = $controller_base_url . "/stats/switches";
    $dpid = json_decode(file_get_contents($get_dpid_url))[0];
    $request_format = array();
    $request_format['dpid'] = $dpid;
    foreach ($request_data as $key => $value) {
        $request_format[$key] = $value;
    }
    $post_url = $controller_base_url . "/stats/flowentry/add";
    $query = json_encode($request_format);
    print_r($request_format);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_URL, $post_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $query);
    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($httpcode == 200) {
        return true;
    }
    return false;
}


function add_filter($data) {
    $data = json_decode($data, true);
    $request = $data['request'];
    if (!validate_request($request)) {
        return false;
    }
    return send_request($data['request']);
}
