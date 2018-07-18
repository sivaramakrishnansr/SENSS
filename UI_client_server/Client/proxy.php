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

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>SENSS</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css">
    <script src="js/jsnetworkx.js"></script>
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
            <a class="navbar-brand" href="ddos_with_sig.php">DDoS with Signature and Proxy</a>
        </div>
    </div>
</nav>
<body>
<!-- This is the image which is generated by the python script which monitors the entire topology
<img src="demo_proxy.png" width="100%" height="100%"> -->

<div id="network-canvas" style="height: 500px; width: 1080px; margin: 0 auto; border: 1px solid black;"></div>

<div class="container inner-container">
    <div class="col-md-8">
        <h2>
            Monitoring Table
        </h2>
    </div>
    <div class="col-md-8">
        <p>Monitor traffic and add/remove rules</p>
	<h4><p>Total traffic: <div id="all_speed">0</div></p></h4>
    </div>
    <div class="col-md-2">
        <p>
            <button type="button" class="btn btn-default" id="add-monitoring-rule">Add Monitoring Rule</button>
            <button type="button" class="btn btn-default" id="add-filter-all">Add filter all</button>
            <button type="button" class="btn btn-default" id="remove-filter-all">Remove filter all</button>
        </p>
    </div>
    <table id="table-monitor" class="table table-bordered table-striped">
        <thead>
        <tr>
            <th>AS Name</th>
            <th>Match</th>
            <!--<th>Packet Count</th>-->
            <!--<th>Byte Count</th>-->
            <th>Speed</th>
            <th>Action</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</div>


<div id="add-monitor-modal" class="modal fade" role="dialog" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                <h4 class="modal-title">Add Monitoring Rule</h4>
            </div>
            <div class="modal-body">
                <table class="table">
                    <tr>
                        <th>
                            <label for="as_name">AS Name:</label>
                        </th>
                        <td>
                            <select id="as_name" class="multiselect-ui form-control" multiple="multiple">

                            </select>
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="nw_src">Source IP:</label>
                        </th>
                        <td>
                            <input type="text" id="nw_src" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="nw_dst">Destination IP:</label>
                        </th>
                        <td>
                            <input type="text" id="nw_dst" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="tcp_src">TCP Source Port:</label>
                        </th>
                        <td>
                            <input type="text" id="tcp_src" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="tcp_dst">TCP Destination Port:</label>
                        </th>
                        <td>
                            <input type="text" id="tcp_dst" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="udp_src">UDP Source Port:</label>
                        </th>
                        <td>
                            <input type="text" id="udp_src" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="udp_dst">UDP Destination Port:</label>
                        </th>
                        <td>
                            <input type="text" id="udp_dst" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="monitor_freq">Monitoring Frequency</label>
                        </th>
                        <td>
                            <input type="text" id="monitor_freq" class="form-control">
                        </td>
                    </tr>

                    <tr>
                        <th>
                            <label for="monitor_duration">Monitoring Duration</label>
                        </th>
                        <td>
                            <input type="text" id="monitor_duration" class="form-control">
                        </td>
                    </tr>
                </table>
            </div>

            <div class="modal-footer">
                <div id="add-monitor-rule" class="btn btn-success">Add Monitoring Rule</div>
            </div>
        </div>
    </div>
</div>
</body>
<script src="js/render_network_ddos_with_sig.js"></script>
<script src="js/script_proxy.js"></script>
</html>
