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
