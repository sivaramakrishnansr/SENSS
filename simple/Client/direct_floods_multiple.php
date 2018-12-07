<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<html>
<head>
          <title>My Form</title>
          <link rel="stylesheet" href="css/bootstrap.min.css">
          <script src="css/jquery.min.js"></script>
          <script src="css/bootstrap.min.js"></script>
   <style>
                .panel { width:300px; margin:auto; padding: 30px;}
                .panel-offset-senss { margin:auto;}
          </style> 
</head>

<body>
        <nav class="navbar navbar-inverse navbar-static-top">
                <div class="container-fluid">
                        <div class="navbar-header">
                                <a class="navbar-brand" href="index.php">SENSS</a>
                        </div>
                        <div>
                                <ul class="nav navbar-nav">
                                        <li><a href="add_filter_form.php">Add Filter</a></li>
                                        <li><a href="get_flows_form.php">Flow Stats</a></li>
                                        <li><a href="get_routes_form.php">Route Stats</a></li>
                                        <li><a href="pic.php">View</a></li>
                                </ul>
                        </div>
                </div>
        </nav>
 <form>

<table>
 <?php
	if($_POST['formSubmit'] == "Submit")
        {
		$o_time= $_POST['o_time'];
		$tag=$_POST['tag'];
		$total_times=$_POST['total_times'];
        	$isp=$_POST['isp'];
        }

	//$o_time= 1;
	//$tag=2;
	//$total_times=3;
        //$isp=4;
        $servername = "localhost";
        $username = "root";
        $password = "usc558l";
       	$dbname = "SENSS";
        $conn = new mysqli($servername, $username, $password, $dbname);

        if ($conn->connect_error) {
               die("Connection failed: " . $conn->connect_error);
	}
	$done=0;
        $sql = "INSERT INTO DIRECT_FLOODS (ID,REQUEST_TO,O_TIME,TOTAL_TIMES,TAG,DONE) VALUES (NULL, '$isp','$o_time','$total_times','$tag','$done')";
	if ($conn->query($sql) === FALSE) {
               echo "Error: " . $sql . "<br>" . $conn->error;
        }
        $conn->close();
	echo "<h1> Waiting for Results</h1>";
	sleep ($o_time);
	header("Location: http://localhost:8181/direct_floods_multiple_view.php");
	exit();

  ?>
</table>

</body>
</html>
