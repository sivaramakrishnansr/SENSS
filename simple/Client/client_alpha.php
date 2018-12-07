
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
            <a class="navbar-brand" href="client_alpha.php">SENSS-Direct Floods without Signature</a>
        </div>
    </div>
</nav>
<body>

<div id="network-canvas" style="height: 500px; width: 1080px; margin: 0 auto; border: 1px solid black;"></div>

<div class="container inner-container">
    <div class="row">
    	<div class="col-sm-4">
        	<h3>Monitoring Table</h3>
    	</div>
    	<div class="col-sm-4">
		<br>
     		<p><b>Traffic Threshold: </b><span id="current-threshold"></span> <span class="pull-right">
     		<button type="button" class="btn btn-primary btn-small" name="submit" id="set-threshold">Edit</button></span></p>
     		<br>
	</div>
    	<div class="col-sm-4">
		<br>
        	<p><b>SENSS nodes: </b><span id="current-nodes"></span> <span class="pull-right"><br>
     		<button type="button" class="btn btn-primary btn-small" name="submit" id="set-nodes">Edit</button></span></p>
		<br>
	</div>
    </div>

    <div class="col-md-8">
	<h4>Total traffic: <span id="all_speed">0</span></h4>
    </div>
    <table id="table-monitor" class="table table-bordered table-striped">
        <thead>
        <tr>
            <th>AS Name</th>
            <th>Speed</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>

<div id="set-threshold-modal" class="modal fade" role="dialog" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h4 class="modal-title">Set Threshold</h4>
            </div>
            <div class="modal-body" style="height:200px;">
                <table class="table">
                    <tr>
                        <td><input type="text" class="form-control" id="threshold-value"></td>
			<td>%</td>
                    </tr>
                </table>
            </div>

            <div class="modal-footer">
                <div id="set-threshold-button" class="btn btn-success">Set Threshold</div>
            </div>
        </div>
    </div>
</div>

<div id="set-nodes-modal" class="modal fade" role="dialog" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h4 class="modal-title">Set Percentage of SENSS nodes</h4>
            </div>
            <div class="modal-body" style="height:200px;">
                <table class="table">
                    <tr>
                        <td><input type="text" class="form-control" id="nodes-value"></td>
			<td>%</td>
                    </tr>
                </table>
            </div>

            <div class="modal-footer">
                <div id="set-nodes-button" class="btn btn-success">Set</div>
            </div>
        </div>
    </div>
</div>
</body>
<script src="js/render_network.js"></script>
<script src="js/script_alpha.js"></script>


</html>
