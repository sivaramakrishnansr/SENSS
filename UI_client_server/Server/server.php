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
            <a class="navbar-brand" href="direct_floods_form.php">SENSS</a>
        </div>
        <div>
            <ul class="nav navbar-nav">
                <li><a href="direct_floods_form.php">Direct Floods</a></li>
            </ul>
        </div>
    </div>
</nav>
<body>

<!--<div id="network-canvas" style="height: 500px; width: 1080px; margin: 0 auto; border: 1px solid black;"></div>-->

<div class="container inner-container">
    <div class="col-md-8">
        <h2>
            Logs
        </h2>
    </div>
    <table id="table-monitor" class="table table-bordered table-striped">
        <thead>
        <tr>
            <th>AS Name</th>
	    <th>Request type</th>
            <th>Match</th>
            <th>Packet Count</th>
            <!--<th>Byte Count</th>-->
            <th>Speed</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>

</body>
<script src="js/script.js"></script>
</html>
