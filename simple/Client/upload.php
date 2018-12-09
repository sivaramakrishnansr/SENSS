<?php
$target_dir = "/var/www/html/SENSS/simple/Client/cert/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
echo $_FILES["fileToUpload"]["tmp_name"]. "\n" . $target_dir;
move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
  echo '<script>window.location.href = "client.php";</script>';
exit;
?>

