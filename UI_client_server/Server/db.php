<?php

$servername1 = "localhost";
$username1 = "root";
$password1 = "usc558l";
$dbname1 = "SENSS";
$conn1 = new mysqli($servername1, $username1, $password1, $dbname1);
if ($conn1->connect_error) {
    die("Connection failed: " . $conn1->connect_error);
}
