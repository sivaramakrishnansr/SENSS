
BASE_URI = "api.php?";
var graph_elements={};

function populateMonitoringTable(nodes) {
    var selectOptionsMarkup = "";
    nodes.forEach(function (node) {
        selectOptionsMarkup += "<option value='" + node + "' name='" + node + "'>" + node + "</option>";
    });
    $("#as_name").append(selectOptionsMarkup);
}

function includeJs(jsFilePath) {
    var js = document.createElement("script");

    js.type = "text/javascript";
    js.src = jsFilePath;

    document.body.appendChild(js);
    console.log("Included JSNX");
}


function renderInitialTopology(topology) {
    //console.log(topology);

    var roots = "";
    var nodes = [];
    topology.self.forEach(function (root) {
        roots += "#" + root + ",";
    });
    roots = roots.slice(0, -1);

    var edges = [];

    topology.nodes.forEach(function (node) {
	//console.log(node);
        if (topology.self.indexOf(node) > -1) {
            nodes.push({data: {id: node, color: 'yellow', border: 'black'}});
        } 
	else {
            nodes.push({data: {id: node, color: 'gray', border: 'black'}});
            topology.self.forEach(function (root) {
                edges.push({data: {id: "root_" + node, name: "", source: root, target: node}});
            });
        }
    });

    var cy = window.cy = cytoscape({
        container: document.getElementById('network-canvas'),
        boxSelectionEnabled: false,
        autounselectify: true,
        layout: {
            name: 'breadthfirst',
            minDist: 10,
            roots: roots
        },

        style: [
            {
                selector: 'node',
                style: {
                    'content': 'data(id)',
                    'text-valign': 'top ',
                    'text-halign': 'center',
                    'background-color': 'data(color)'
                }
            },

            {
                selector: '#cloud',
                style: {
                    'content': 'data(id)',
                    'background-image': 'images/cloud.jpeg',
                    'shape': 'rectangle',
                    'background-fit': 'cover',
                    'width': '720px',
                    'height': '480px'
                }
            },

            {
                selector: 'edge',
                style: {
                    'content': 'data(name)',
                    'curve-style': 'bezier',
                    'width': 2,
                    'line-style': 'dashed',
                    'line-color': 'black',
                    'text-margin-y': -20
                }
            }
        ],

        elements: {
            nodes: nodes,
            edges: edges
        }
    });

    cy.on('mouseover', 'node', function(event) {
        var node = event.target;
        node.qtip({
            content: node.id(),
            show: {
                event: event.type,
                ready: true
            },
            hide: {
                event: 'mouseout unfocus'
            }
        }, event);
    });
    topology.monitoring_rules.forEach(function (rule) {
        //var as_monitor_info = {
        //    match: rule[1],
        //    frequency: rule[2],
        //    end_time: rule[3],
        //    monitor_id: rule[4]
        //};
        var as_monitor_info = {
            match: rule["match_field"],
            frequency: rule["frequency"],
            end_time: rule["end_time"],
            monitor_id: rule["monitor_id"]
        };

        //poll_stats(rule[0], rule[4], JSON.parse(rule[1]));
        poll_stats(rule["as_name"], rule["monitor_id"], JSON.parse(rule["match_field"]));

        /*var random = Math.random().toString(36).substring(7);
        var markup = "<tr><td>" + rule[0] + "</td><td><pre>" + JSON.stringify(JSON.parse(rule[1]), undefined, 4) +
            "</pre></td><td id='packet-count-" + random + "'></td><td id='byte-count-" + random + "'></td>" +
            "<td id='speed-" + random + "'></td><td><button type='button' class='btn btn-success'>" +
            "Add Filter</button></td></tr>";
        $("#table-monitor").append(markup);

        var timer = setInterval(function () {
            if (Math.floor(Date.now() / 1000) > rule[3]) {
                clearInterval(timer);
            }

            $.ajax({
                url: BASE_URI + "get_monitor&as_name=" + rule[0],
                type: "POST",
                data: JSON.stringify(JSON.parse(rule[1]).match),
                success: function (result) {
                    populateMonitoringValues(random, JSON.parse(result));
                }
            });
        }, (parseInt(rule[2])) * 1000); // rule[2] is actual frequency with which the backend system will update the database/
        // We give couple more seconds to reflect the data in the DB and then fetch the updated data.*/
    });
}

function getTopologyData() {
    $.ajax({
        url: BASE_URI + "topology",
        success: function (result) {
            var topology = JSON.parse(result);
            populateMonitoringTable(topology.nodes);
            renderInitialTopology(topology);
        }
    });
}

getTopologyData();
