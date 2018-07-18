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
	header('Content-Type: application/json');
        switch($_POST['functionname']) {
            		case 'insert_threshold':
				$threshold=$_POST['arguments'][0];
		    		require_once "db.php";
    		    		$sql = sprintf("SELECT * FROM CLIENT_LOGS");
    				$result = $conn1->query($sql);
    				$id = 0;
    				if ($result->num_rows > 0) {
        				while ($row = $result->fetch_assoc()) {
 		       				$id = $row['id'];
        					$sql = sprintf("UPDATE CLIENT_LOGS SET threshold = %d WHERE id = %d",
            						$threshold, $id);
					        $conn1->query($sql);
        					$conn1->commit();
					}
    				}
    				$conn1->close();
    				echo json_encode(array("success"=>true),true);
				break;
			case 'get_threshold':
				require_once "db.php";
    				$sql = sprintf("SELECT threshold FROM CLIENT_LOGS");
    				$result = $conn1->query($sql);
    				$id = 0;
    				if ($result->num_rows == 1) {
        				$threshold = $result->fetch_assoc()['threshold'];
    				}
    				$conn1->close();
    				echo json_encode(array("succcess"=>true,"threshold"=>$threshold),true);
				break;
	}


?>
