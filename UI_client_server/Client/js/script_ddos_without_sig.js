
var threshold = 0;
var storednodes=0;
var proxy_counter = 0;
var proxy_flag=0;
var sum_array={"hpc039":{},"hpc041":{},"hpc042":{},"hpc043":{},"hpc044":{},"hpc046":{},"hpc047":{},"hpc048":{},"hpc049":{},"hpc050":{},"hpc052":{},"hpc054":{},"hpc056":{},"hpc057":{}}
var traffic_contribution={"hpc039":0,"hpc041":0,"hpc042":0,"hpc043":0,"hpc044":0,"hpc046":0,"hpc047":0,"hpc048":0,"hpc049":0,"hpc050":0,"hpc052":0,"hpc054":0,"hpc056":0,"hpc057":0}
var monitoring_rules={};
var monitor_ids={};
var global_speed=0;
var monitor_ids_available=false;
var filter_on=false;
var random_nodes;


function includeJs(jsFilePath) {
	var js = document.createElement("script");
	js.type = "text/javascript";	
	js.src = jsFilePath;
	document.body.appendChild(js);
}

//Generates random SENSS nodes based on client specifications
function getRandom(n) {
	var arr = [];
	for (var i = 1; i <= myConstClass.number_of_nodes; i++) {
		arr.push(i);
	}
    	var result = new Array(n),
        len = arr.length,
        taken = new Array(len);
    	if (n > len)
        	throw new RangeError("getRandom: more elements taken than available");
    	while (n--) {
        	var x = Math.floor(Math.random() * len);
        	result[n] = arr[x in taken ? taken[x] : x];
        	taken[x] = --len in taken ? taken[len] : len;
    	}
    	return result;
}

//Populating current traffic rate at the client
function populateMonitoringValues(rowId, as_name, data) {
	if (data.speed=="Not reachable"){
		console.log("SENSS: SENSS server not reachable");
    	}
	else{
		if (!(rowId in sum_array[as_name])){
			sum_array[as_name][rowId]=0;
		}
		sum_array[as_name][rowId]=data.speed;
    		$("#packet-count-" + rowId).html(data.packet_count);
    		$("#speed-" + rowId).html(display_threshold(data.speed));
		var as_speed=0;
		for (var key in sum_array[as_name]){
			as_speed=as_speed+Number(sum_array[as_name][key]);
		}
    		if (parseInt(data.speed) >= 35*1000*1000*1000) {
        		cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "red");
    		} else {
        		cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "green");
    		}
		for (var as_name in sum_array){
			for (var row in sum_array[as_name]){
				monitoring_rules[row]["speed"]=sum_array[as_name][row];
			}
		}

		//Calculates the shortest path from nodes to SENSS client and estimates the amount of traffic sent to them
		var edge_speeds={};
		for (var as_name in graph_elements){
			edge_speeds[as_name]={};
			var nodes=graph_elements[as_name].nodes();
			for(var n=0;n<nodes.length;n++){
				var node=nodes[n];
				if(node==0){
					continue;
				}
				var shortest_path=jsnx.bidirectionalShortestPath(graph_elements[as_name],0,node);
				var exists=0;
				for (var i=0;i<shortest_path.length;i++){
					var in_node=shortest_path[i];
					if(random_nodes.indexOf(in_node)>-1){
						exists=exists+1;
					}
				}
				for(var rid in monitoring_rules){
					if(monitoring_rules[rid]["src_ip"]==Number(node) && monitoring_rules[rid]["as_name"]==as_name){
						if(exists>=1){
							monitoring_rules[rid]["can_block"]=true;
						}
						var node_speed=monitoring_rules[rid]["speed"];
					}
				}
				for(var i=0;i<shortest_path.length;i++){
					if(i+1==shortest_path.length){
						break;
					}
					var node_1=shortest_path[i];
					var node_2=shortest_path[i+1];
					var min_node;
					var max_node;
					if(node_1>node_2){
						min_node=node_2;
						max_node=node_1;
					}else{
						min_node=node_1;
						max_node=node_2;
					}
					var edge=min_node+"_"+max_node;
					if(!(edge in edge_speeds[as_name])){
						edge_speeds[as_name][edge]=0;
					}
					edge_speeds[as_name][edge]=edge_speeds[as_name][edge]+Number(node_speed);
				}
			}
		}
			

		//Updates the traffic rates on the edges 
		for (var as_name in graph_elements){
			var all_edges=graph_elements[as_name].edges();
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
				if(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge])>=0){
		        		cy.$("#"+as_name+"_"+min_edge+"_"+max_edge).data("name", display_threshold(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge]))).style("line-color", "green");
				}else{
		        		cy.$("#"+as_name+"_"+min_edge+"_"+max_edge).data("name", display_threshold(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge]))).style("line-color", "black");
				}
			}
			var as_speed=0;
			for (var key in sum_array[as_name]){
				as_speed=as_speed+Number(sum_array[as_name][key]);
			}
			if(parseInt(as_speed)>=0){
		        	cy.$("#"+as_name+"_"+as_name+"_0").data("name", display_threshold(parseInt(as_speed))).style("line-color", "green");
			}else{
		        	cy.$("#"+as_name+"_"+as_name+"_0").data("name", display_threshold(parseInt(as_speed))).style("line-color", "black");
			}
		}
    	}
    	var all_speed=0;
    	var all_byte_count=0;
    	for (var key1 in sum_array){
		for(var key2 in sum_array[key1]){
			all_speed=all_speed+Number(sum_array[key1][key2]);
		}
	}
    	global_speed=all_speed;
    	$("#all_speed").html(display_threshold(all_speed));
}

//Detects the signature change in traffic and add filter rules based on the threshold of traffic which the SENSS client is willing to loose
//By default, an attack is triggered when the threshold of incoming traffic is exceeded beyong 10Gbps. But this could be altered for different testing scenarios
function auto_detection(){
    	for(var as_name in sum_array){
		for(var r=1;r<=myConstClass.number_of_nodes;r++){
			if (random_nodes.indexOf(r)>-1){
	    			cy.$("#"+as_name+"_"+r).data("color","red");
			}else{
	    			cy.$("#"+as_name+"_"+r).data("color","gray");
			}
		}
    	}

	var attack_flag=0;
    	if (global_speed/1000000000>100 || filter_on==true){
		attack_flag=1;
    	}
    	else{
		attack_flag=0;
    	}
    	var contribution_map={}
    	for (var key in monitoring_rules){
		as_speed=monitoring_rules[key]["speed"];
		contribution=Number(as_speed)/global_speed*100;
		if (attack_flag==1){
			if (monitoring_rules[key]["contribution"]<=threshold){
				contribution_map[key]=monitoring_rules[key]["contribution"];
			}
		}else{
			monitoring_rules[key]["contribution"]=contribution;
		}
   	}
	var new_contribution_map = Object.keys(contribution_map).map(function(key) {
   		return [key, contribution_map[key]];
	});
	new_contribution_map.sort(function(first, second) {
    		return second[1] - first[1];
   	});   
   	new_contribution_map.reverse();
   	var arrayLength = new_contribution_map.length;
   	var canBlock=[];
   	var legit_loss=0;
   	for (var i = 0; i < arrayLength; i++) {
		var temp_legit_loss=legit_loss+new_contribution_map[i][1];
		if (temp_legit_loss<threshold){
			legit_loss=legit_loss+new_contribution_map[i][1];
			canBlock.push(new_contribution_map[i][0]);
		}
   	}
   	for (var rowID in monitoring_rules){
		var monitor_id=monitoring_rules[rowID]["monitor_id"];
		var as_name=monitoring_rules[rowID]["as_name"];
		var has_filter=monitoring_rules[rowID]["filter"];
		var src_ip=monitoring_rules[rowID]["src_ip"];
		var can_block_flag=monitoring_rules[rowID]["can_block"];

		if (canBlock.indexOf(rowID)==-1){
			if(has_filter==true){
		        	$.ajax({
					'async': false,
            				url: BASE_URI + "remove_filter&as_name=" + as_name + "&monitor_id=" + monitor_id,
            				type: "GET",
            				success: function (result) {
						monitoring_rules[rowID]["filter"]=false;
            				}
				});
			}
		}
		if(canBlock.indexOf(rowID)>-1){
			if(has_filter==false && can_block_flag==true){
		        	$.ajax({
					'async': false,
            				url: BASE_URI + "add_filter&as_name=" + as_name + "&monitor_id=" + monitor_id,
            				type: "GET",
            				success: function (result) {
						monitoring_rules[rowID]["filter"]=true;
            				}
				});
			}
		}
    	}
   	var total=0;
   	for (var rowID in monitoring_rules){
		if (monitoring_rules[rowID]["filter"]==true){
			filter_on=true;
			total=total+1;
		}
   	}
   	if (total==0){
		filter_on=false;
   	}
}

//Polls the SENSS servers for traffic rates on flows based on monitoring rules which are added
function poll_stats(as_name, monitor_id, as_monitor_info) {
    	monitoring_rules[random]={};
    	monitoring_rules[random]["as_name"]=as_name;
    	monitoring_rules[random]["monitor_id"]=monitor_id;
    	monitoring_rules[random]["filter"]=false;
    	var src_ip=as_monitor_info.match.ipv4_src.split(".")[3];
    	monitoring_rules[random]["src_ip"]=Number(src_ip);
	monitoring_rules[random]["can_block"]=false;

	var random = Math.random().toString(36).substring(7);
    	var markup = "<tr id='monitor-row-" + random +"'><td>" + as_name+ "_"+src_ip+"</td>"+
		     "<td id='speed-" + random + "'></td></tr>;"
    	$("#table-monitor").append(markup);
    	var timer = setInterval(function () {
        	if (Math.floor(Date.now() / 1000) > as_monitor_info.end_time) {
            		clearInterval(timer);
        	}
        	$.ajax({
            		url: BASE_URI + "get_monitor&as_name=" + as_name + "&monitor_id=" + monitor_id,
            		type: "GET",
            		error: function () {
	    			var error_data={packet_count:"Not reachable",speed:"Not reachable"};
	    			var error_data={packet_count:0,speed:0};
            			populateMonitoringValues(random, as_name, error_data);
            		},
            		success: function (result) {
				if (typeof result !== 'undefined') {
					var iii=0;
				}
                		var resultParsed = JSON.parse(result);
                		if (resultParsed.success) {
                    			populateMonitoringValues(random, as_name, resultParsed.data);
                		}
            		},
	    		timeout: 2000
        	});
        }, (parseInt(as_monitor_info.frequency) + 2) * 1000); 

    	var auto_detection_times=setInterval(function() {
		auto_detection();	
	}, (parseInt(as_monitor_info.frequency) + 2) * 1000);

    	monitoring_rules[random]={};
    	monitoring_rules[random]["as_name"]=as_name;
    	monitoring_rules[random]["monitor_id"]=monitor_id;
    	monitoring_rules[random]["filter"]=false;
    	var src_ip=as_monitor_info.match.ipv4_src.split(".")[3];
    	monitoring_rules[random]["src_ip"]=Number(src_ip);
	monitoring_rules[random]["can_block"]=false;
}

//Creates the traffic rates in readable format
function display_threshold(int_threshold) {
	var zeros = parseInt(Math.log(int_threshold) / Math.log(10));
    	if (zeros >= 12) {
        	return (int_threshold / Math.pow(10, 12)).toFixed(2).toString() + " TBps";
    	} else if (zeros >= 9) {
        	return (int_threshold / Math.pow(10, 9)).toFixed(2).toString() + " GBps";
    	} else if (zeros >= 6) {
        	return (int_threshold / Math.pow(10, 6)).toFixed(2).toString() + " MBps";
    	} else if (zeros >= 3) {
        	return (int_threshold / Math.pow(10, 3)).toFixed(2).toString() + " KBps";
    	} else {
        	return int_threshold.toString() + " Bps";
    	}
}


function set_threshold() {
	var storedThreshold = localStorage.getItem("threshold");
    	if (storedThreshold != null) {
        	threshold = parseInt(storedThreshold);
    	}
    	$("#current-threshold").html(threshold+"%");
}

function senss_nodes() {
	var storednodes1 = localStorage.getItem("nodes");
    	if (storednodes1 != null) {
        	storednodes = parseInt(storednodes1);
    	}
    	$("#current-nodes").html(storednodes+"%");
    	random_nodes=getRandom(Math.floor(Number(storednodes)*myConstClass.number_of_nodes/100));
}

//Adds initial rules for monitoring when the SENSS Client is loaded. Does not add monitoring rules if monitoring rules are already present
function add_initial_rules(){
	$.ajax({
        	url: BASE_URI + "get_monitor_ids",
            	type: "GET",
            	success: function (result) {
			if (result== "{}"){
				monitor_ids_available=false;
			        for (var key in sum_array){
					for (i = 1; i <=myConstClass.number_of_nodes; i++) {
				                var as_int=key.replace("hpc0","");
						var key_array=[key];
                				var data = {
                        				as_name: key_array,
	               					 match: {
        	                				ipv4_src: as_int+".0.0."+i.toString(),
                	        				ipv4_dst: "57.0.0.1",
                        					tcp_src: 0,
                        					tcp_dst: 0,
                        					udp_src: 0,
                        					udp_dst: 0
	        		            		},
        	            				monitor_frequency: 1,
				                    	monitor_duration: 10000,
							monitor_type: "init"
				                };
				                $.ajax({
                       		 			url: BASE_URI + "add_monitor",
				                        type: "POST",
				                        data: JSON.stringify(data),
				                        contentType: "application/json",
				                        dataType: "json",
				                        success: function (result) {
				                                result.as_name_id.forEach(function (as_name_id) {
					                                poll_stats(as_name_id.as_name, as_name_id.monitor_id, result.match);
				                                });
				                        }
				                });
		        	        }
			        }

			}
			else{
				monitor_ids=JSON.parse(result);
				monitor_ids_available=true;
			}
            }
        });
}

$(document).ready(function () {
    	add_initial_rules();
    	set_threshold();
    	senss_nodes();
    
	//Sets the threshold of traffic which the SENSS client is willing to loose
    	$("#set-threshold").click(function () {
        	$("#set-threshold-modal").modal('show');
    	});

	//Sets the number of SENSS servers in the experiment
    	$("#set-nodes").click(function () {
        	$("#set-nodes-modal").modal('show');
    	});


    	$("#set-threshold-button").click(function () {
        	var value = parseInt($("#threshold-value").val());
		threshold=value;
        	localStorage.setItem("threshold", threshold);
        	$("#current-threshold").html(threshold+"%");
        	$("#set-threshold-modal").modal('hide');
    	});

    	$("#set-nodes-button").click(function () {
        	var value = parseInt($("#nodes-value").val());
		storednodes=value;
        	localStorage.setItem("nodes", storednodes);
        	$("#current-nodes").html(storednodes+"%");
        	$("#set-nodes-modal").modal('hide');
		random_nodes=getRandom(Math.floor(Number(value)*myConstClass.number_of_nodes/100));
	    	for(var as_name in sum_array){
			for(var r=1;r<=myConstClass.number_of_nodes;r++){
				if (random_nodes.indexOf(r)>-1){
	    				cy.$("#"+as_name+"_"+r).data("color","red");
				}else{
	    				cy.$("#"+as_name+"_"+r).data("color","gray");
				}
			}
			for(var r=0;r<random_nodes.length;r++){
				var ran=random_nodes[r];
			}
    		}
    	});
});

