<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    	<title>SENSS</title>
    	<link rel="stylesheet" href="css/bootstrap.min.css">
    	<link rel="stylesheet" href="css/style.css">
   	<script src="js/jquery.min.js"></script>
    	<script src="js/bootstrap.min.js"></script>
    	<script src="js/cytoscape.min.js"></script>
    	<script src="js/jquery.qtip.min.js"></script>
    	<link rel="stylesheet" href="css/jquery.qtip.min.css">
    	<script src="js/cytoscape-qtip.js"></script>
    	<style>
        	.panel {
            		width: 300px;
            		margin: auto;
            		padding: 30px;
        	}

        	.panel-offset-senss {
            		margin: auto;
        	}

        	.second-button {
            		float: right;
       	 	}
    	</style>
</head>

<body>
<nav class="navbar navbar-inverse navbar-static-top">
    <div class="container-fluid">
        <div class="navbar-header">
            <a class="navbar-brand" href="client.php">Setup</a>
            <a class="navbar-brand" href="ddos_with_sig.php">SENSS Client</a>
            <a class="navbar-brand" href="logs.php">Logs</a>
        </div>
    </div>
</nav>
<body>


<div class="container inner-container">
    	<div class="col-md-8">
        	<h2>Logs</h2>
    	</div>
    	<table id="table-monitor" class="table table-bordered table-striped">
        	<thead>
        	<tr>
	    		<th>Request type</th>
            		<th>Match</th>
	    		<th>Number of requests</th>
        	</tr>
       	 	</thead>
        <tbody>
        </tbody>
    </table>
</div>



</body>
<script src="js/script.js"></script>
</html>
