<?php
    require_once "db_conf.php";
    $sql = "SELECT as_name, server_url FROM AS_URLS";
    //$sql = "SELECT as_name, server_url FROM AS_URLS WHERE as_name in ('" .$input['as_name'] . "')";
    $result = $conn->query($sql);
    while ($row = $result->fetch_assoc()) {
        print_r($row);
        echo "\n";
    }
?>
