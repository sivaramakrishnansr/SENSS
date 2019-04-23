<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>SENSS</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <script src="js/jsnetworkx.js"></script>
    <script src="js/constants.js"></script>
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
            <a class="navbar-brand" href="amon.php">AMON-SENSS</a>
        </div>
    </div>
</nav>
<body>

<div id="network-canvas" style="height: 500px; width: 1080px; margin: 0 auto; border: 1px solid black;"></div>

<div class="container inner-container">
    <div class="row">
    	<div class="col-md-8">
        	<h3>AMON-SENSS Monitoring Table</h3>
    	</div>
    </div>

    <div class="col-md-8">
	<h4>Total traffic: <span id="all_speed">0</span></h4>
    </div>

    <div class="col-md-8">
	<h4>Proxy Reachable: <span id="proxy_tag"></span></h4>
    </div>

    <table id="table-monitor" class="table table-bordered table-striped">
        <thead>
        <tr>
            <th>SENSS server</th>
            <th>Recommended filter</th>
	    <th>Status</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>


</body>
<script src="js/render_network_amon.js"></script>
<script src="js/script_amon.js"></script>


</html>
