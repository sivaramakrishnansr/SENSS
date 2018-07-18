<!--
#
# Copyright (C) 2018 University of Southern California.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
-->

<?php

function get_server_logs()
{
    	require_once "db.php";
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
?>
