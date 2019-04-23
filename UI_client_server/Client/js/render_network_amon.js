BASE_URI = "api.php?";
var graph_elements={};
var node_names=["AboveNet", "AGIS", "ANS", "Bandcon", "BBNplanet", "Bestel", "BTN", "Claranet" ,"Cogent", "DT", "Epoch", "GetNet", "IBM", "iSTAR", "Netrail", "OTEGlobe", "PalmettoNet", "Quest", "Sprint", "Tinet", "ESnet", "Heanet", "LATNET", "NSF", "Zamren","AT&T","Airtel","Reliance"]
var node_index_counter=0;
var node_mapper={};
var node_name;
var root_name;



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
        console.log(node,topology.self.indexOf(node));
        if (topology.self.indexOf(node) > -1) {
            nodes.push({data: {id: node, color: 'yellow', border: 'black'}});
        }
        else {
	    nodes.push({data: {id: node, color: 'gray', border: 'black'}});

            	var G = jsnx.binomialGraph(myConstClass.number_of_nodes+1,0.3);
	            for(var i=1;i<=myConstClass.number_of_nodes;i++){
        	        if(jsnx.hasPath(G, {source: 0, target: i})==false){
                	        G.addEdge(0,i);
	                }
        	    }
	    if (node=="hpc050"){
	            var G=new jsnx.Graph();
	            G.addNodesFrom([0,1,2,3,4,5,6,7]);
        	    G.addEdge(0,1);	    
	            G.addEdge(0,2);	    
        	    G.addEdge(0,3);	    
	            G.addEdge(1,4);	    
	            G.addEdge(2,5);	    
	            G.addEdge(5,6);	    
	            G.addEdge(5,7);	    
            }

	    if (node=="hpc054"){
	            var G=new jsnx.Graph();
	            G.addNodesFrom([0,1,2,3,4,5,6,7]);
        	    G.addEdge(0,1);	    
	            G.addEdge(0,2);	    
        	    G.addEdge(0,3);	    
        	    G.addEdge(0,4);	    
        	    G.addEdge(1,5);	    
        	    G.addEdge(2,6);
        	    G.addEdge(3,7);	    
        	    G.addEdge(3,5);	    
        	    G.addEdge(6,7);	    
        	    G.addEdge(2,7);	    
            }

	    if (node=="hpc052"){
	            var G=new jsnx.Graph();
	            G.addNodesFrom([0,1,2,3,4,5,6,7]);
        	    G.addEdge(0,1);	    
	            G.addEdge(0,2);	    
        	    G.addEdge(2,3);	    
        	    G.addEdge(2,4);	    
        	    G.addEdge(2,5);	    
        	    G.addEdge(2,6);
        	    G.addEdge(3,4);	    
        	    G.addEdge(5,6);	    
        	    G.addEdge(4,7);	    
            }


	    //Add the subgraph to graph elements for path calculations
            graph_elements[node]=G;

	    //Add the nodes to main topology with the naming convention
            var all_nodes=G.nodes();
            for (var i=0;i<all_nodes.length;i++){
                    var sub_node=node+"_"+all_nodes[i];
                    nodes.push({data: {id: sub_node, color: 'gray', border: 'black'}});
            }

	    //Add the node to the root of the topology
            topology.self.forEach(function (root) {
                edges.push({data: {id: "root_" + node, name: "", source: root, target: node}});
            });

	    //Push the edges with the naming convention to the main graph
            var all_edges=G.edges();
            for (var i=0;i<all_edges.length;i++){
                        var sub_edge=all_edges[i];
                        var min_edge;
                        var max_edge;
                        if (sub_edge[0]>sub_edge[1]){
                                min_edge=sub_edge[1];
                                max_edge=sub_edge[0];
                        }
                        else{
                                max_edge=sub_edge[1];
                                min_edge=sub_edge[0];
                        }
                        edges.push({data: {id: node+"_"+min_edge+"_"+max_edge, name: "", source: node+"_"+min_edge, target: node+"_"+max_edge}});
            }
	    //Connect the first node to the main node in consideration
            edges.push({data: {id: node+"_"+node+"_"+0, name: "", source: node+"_"+0, target: node}});
	
	    /*
	    //Randomly generate graphs within and see if there is a path to the main root node. If there is no path, then attach to the root itself.
            var G = jsnx.binomialGraph(myConstClass.number_of_nodes+1,0.3);
            for(var i=1;i<=myConstClass.number_of_nodes;i++){
                if(jsnx.hasPath(G, {source: 0, target: i})==false){
                        G.addEdge(0,i);
                }
            }
	    //Add the subgraph to graph elements for path calculations
            graph_elements[node]=G;

	    //Add the nodes to main topology with the naming convention
            var all_nodes=G.nodes();
            for (var i=0;i<all_nodes.length;i++){
                    var sub_node=node+"_"+all_nodes[i];
                    nodes.push({data: {id: sub_node, color: 'gray', border: 'black'}});
            }

	    //Add the node to the root of the topology
            topology.self.forEach(function (root) {
                edges.push({data: {id: "root_" + node, name: "", source: root, target: node}});
            });

	    //Push the edges with the naming convention to the main graph
            var all_edges=G.edges();
            for (var i=0;i<all_edges.length;i++){
                        var sub_edge=all_edges[i];
                        var min_edge;
                        var max_edge;
                        if (sub_edge[0]>sub_edge[1]){
                                min_edge=sub_edge[1];
                                max_edge=sub_edge[0];
                        }
                        else{
                                max_edge=sub_edge[1];
                                min_edge=sub_edge[0];
                        }
                        edges.push({data: {id: node+"_"+min_edge+"_"+max_edge, name: "", source: node+"_"+min_edge, target: node+"_"+max_edge}});
            }
	    //Connect the first node to the main node in consideration
            edges.push({data: {id: node+"_"+node+"_"+0, name: "", source: node+"_"+0, target: node}});
	    */
        }
    });
    nodes.push({data: {id: "proxy", color: 'purple', border: 'black'}});
    edges.push({data: {id: "proxy_link" , name: "", source: "hpc057", target: "proxy"}});
    //Map the names finally
    for (var i = 0; i < nodes.length; i++){
		if(nodes[i].data.id=="proxy"){
			nodes[i].data.name="Proxy at Sprint";
			
			continue;
		}
		nodes[i].data.name=node_names[i];
		node_mapper[nodes[i].data.id]=node_names[i];
		//console.log(nodes[i]);
	}



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
                    'content': 'data(name)',
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



    /*cy.on('mouseover', 'node', function(event) {
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
    });*/
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
includeJs("js/jsnetworkx.js");
getTopologyData();
