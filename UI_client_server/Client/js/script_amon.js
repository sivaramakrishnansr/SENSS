var exclude_speeds={};
var filter_obtained_dict={}
var filter_added_dict={}
var threshold = 0;
var storednodes=0;
var proxy_counter = 1;
var proxy_flag=0;
var sum_array={"hpc039":{},"hpc041":{},"hpc042":{},"hpc043":{},"hpc044":{},"hpc046":{},"hpc047":{},"hpc048":{},"hpc049":{},"hpc050":{},"hpc052":{},"hpc054":{},"hpc056":{},"hpc057":{}}
var traffic_contribution={"hpc039":0,"hpc041":0,"hpc042":0,"hpc043":0,"hpc044":0,"hpc046":0,"hpc047":0,"hpc048":0,"hpc049":0,"hpc050":0,"hpc052":0,"hpc054":0,"hpc056":0,"hpc057":0}
var monitoring_rules={};
var monitor_ids={};
var global_speed=0;
var monitor_ids_available=false;
var filter_on=false;
var random_nodes;
var row_ids={}
var proxy_threshold=40;

function objectEquals(x, y) {
    'use strict';

    if (x === null || x === undefined || y === null || y === undefined) { return x === y; }
    // after this just checking type of one would be enough
    if (x.constructor !== y.constructor) { return false; }
    // if they are functions, they should exactly refer to same one (because of closures)
    if (x instanceof Function) { return x === y; }
    // if they are regexps, they should exactly refer to same one (it is hard to better equality check on current ES)
    if (x instanceof RegExp) { return x === y; }
    if (x === y || x.valueOf() === y.valueOf()) { return true; }
    if (Array.isArray(x) && x.length !== y.length) { return false; }

    // if they are dates, they must had equal valueOf
    if (x instanceof Date) { return false; }

    // if they are strictly equal, they both need to be object at least
    if (!(x instanceof Object)) { return false; }
    if (!(y instanceof Object)) { return false; }

    // recursive object equality check
    var p = Object.keys(x);
    return Object.keys(y).every(function (i) { return p.indexOf(i) !== -1; }) &&
        p.every(function (i) { return objectEquals(x[i], y[i]); });
}

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
function populateMonitoringValues(rowId, as_name, data, as_monitor_info) {
	if (as_monitor_info.match.ipv4_src=="52.0.0.1" || as_monitor_info.match.ipv4_src=="52.0.0.2" || as_monitor_info.match.ipv4_src=="52.0.0.3" || as_monitor_info.match.ipv4_src=="52.0.0.4"){
		//console.log(as_monitor_info.match);
		//console.log(data);
	}
	if (data.packet_count=="Not reachable"){
                if (!(rowId in sum_array[as_name])){
                        sum_array[as_name][rowId]=0;
                }
                //$("#speed-" + rowId).html("N/A");
                $("#speed-" + rowId).html("0 Bps");
                //cy.$("#root_" + as_name).data("name", "N/A").style("line-color", "#996300");
                //cy.$("#root_" + as_name).data("name", "0 Bps").style("line-color", "green");
                //proxy_counter=proxy_counter+1;
		//console.log("PROXY COUNTER "+proxy_counter);
    	}
	else{
		if (global_speed>=40000000000){
			proxy_counter=proxy_counter+1;
			console.log("PROXY COUNTER "+proxy_counter);
		}		
		if (!(rowId in sum_array[as_name])){
			sum_array[as_name][rowId]=0;
		}


		//Gets updated here
		//Need to update this ONLY when the node is present beyond the point
		sum_array[as_name][rowId]=data.speed;

    		$("#packet-count-" + rowId).html(data.packet_count);
    		$("#speed-" + rowId).html(display_threshold(data.speed));

		var original_as_name=as_name;


		for (var as_name in sum_array){
			for (var row in sum_array[as_name]){
				monitoring_rules[row]["speed"]=sum_array[as_name][row];
			}
		}

		//Calculates the shortest path from nodes to SENSS client and estimates the amount of traffic sent to them
		var edge_speeds={};
		for (var as_name in graph_elements){
			exclude_speeds[as_name]=[];
			edge_speeds[as_name]={};
			var nodes=graph_elements[as_name].nodes();
			for(var n=0;n<nodes.length;n++){
				var node=nodes[n];
				if(node==0){
					continue;
				}
				//Finding the shortest path to node 0
				var shortest_path=jsnx.bidirectionalShortestPath(graph_elements[as_name],0,node);
				shortest_path=shortest_path.reverse();
				//console.log(shortest_path+" shortest path");
				var exists=0;
				for (var i=0;i<shortest_path.length;i++){
					var in_node=shortest_path[i];
					if(random_nodes.indexOf(node_mapper[as_name+"_"+in_node])>-1){
					//if(random_nodes.indexOf(in_node)>-1){
						exists=exists+1;
					}
				}
				for(var rid in monitoring_rules){
					if(monitoring_rules[rid]["src_ip"]==Number(node) && monitoring_rules[rid]["as_name"]==as_name){
						if(exists>=1){
							monitoring_rules[rid]["can_block"]=true;
						}
						//markhere
						var node_speed=monitoring_rules[rid]["speed"];
						var valid_rid=rid;
					}
				}
				var to_include=true;
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
					if (to_include==true){
						edge_speeds[as_name][edge]=edge_speeds[as_name][edge]+Number(node_speed);
					}

					if(random_nodes.indexOf(node_mapper[as_name+"_"+node_2])>-1 && as_name in filter_added_dict){
						if(filter_added_dict[as_name].indexOf(valid_rid)>-1){
							to_include=false;
							exclude_speeds[as_name].push(valid_rid);
						}
					}

					if(random_nodes.indexOf(node_mapper[as_name+"_"+node_2])>-1 && as_name in filter_obtained_dict){
						if(filter_obtained_dict[as_name].indexOf(valid_rid)>-1){
							var row = document.getElementById('as-name-'+valid_rid);
							row.innerHTML=node_mapper[as_name+"_"+node_2];
						}
					}
					
				}
			}
		}
		//console.log(edge_speeds);

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
				if(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge])>0 && parseInt(edge_speeds[as_name][min_edge+"_"+max_edge])< 5.5*1000*1000*1000){
		        		cy.$("#"+as_name+"_"+min_edge+"_"+max_edge).data("name", display_threshold(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge]))).style("line-color", "green");
				}
				if(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge])>=5.5*1000*1000*1000){
		        		cy.$("#"+as_name+"_"+min_edge+"_"+max_edge).data("name", display_threshold(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge]))).style("line-color", "red");
				}
				if(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge])==0){
		        		cy.$("#"+as_name+"_"+min_edge+"_"+max_edge).data("name", display_threshold(parseInt(edge_speeds[as_name][min_edge+"_"+max_edge]))).style("line-color", "black");
				}
			}

			if (as_name==original_as_name){
				var as_speed=0;
				for (var key in sum_array[as_name]){
					if(exclude_speeds[as_name].indexOf(key)>-1){
						continue;
					}
					as_speed=as_speed+Number(sum_array[as_name][key]);
				}

    				if (parseInt(as_speed) >= 5.5*1000*1000*1000) {
		        		cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "red");
    				} 
	
				if (parseInt(as_speed)>0 && parseInt(as_speed) < 5.5*1000*1000*1000){
        				cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "green");
		    		}

				if (parseInt(as_speed)==0){
		        		cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "black");
    				}
			}
			//This controls the final edges and gets the update from sum array
			var as_speed=0;
			for (var key in sum_array[as_name]){
				if(exclude_speeds[as_name].indexOf(key)>-1){
					continue;
				}
				as_speed=as_speed+Number(sum_array[as_name][key]);

			}
			if(parseInt(as_speed)>0 && parseInt(as_speed)<5.5*1000*1000*1000){
		        	cy.$("#"+as_name+"_"+as_name+"_0").data("name", display_threshold(parseInt(as_speed))).style("line-color", "green");
			}
			if(parseInt(as_speed)>=5.5*1000*1000*1000){
		        	cy.$("#"+as_name+"_"+as_name+"_0").data("name", display_threshold(parseInt(as_speed))).style("line-color", "red");

			}
			if (parseInt(as_speed)==0){
		        	cy.$("#"+as_name+"_"+as_name+"_0").data("name", display_threshold(parseInt(as_speed))).style("line-color", "black");
			}
		}
    	}
    	var all_speed=0;
    	var all_byte_count=0;
    	for (var key1 in sum_array){
		for(var key2 in sum_array[key1]){
			if (key1 in exclude_speeds){
				if(exclude_speeds[key1].indexOf(key2)>-1){
					continue;
				}
			}

			all_speed=all_speed+Number(sum_array[key1][key2]);
		}
	}
    	global_speed=all_speed;
    	$("#all_speed").html(display_threshold(all_speed));
}



//Polls the SENSS servers for traffic rates on flows based on monitoring rules which are added
function poll_stats(as_name, monitor_id, as_monitor_info) {
	var random = Math.random().toString(36).substring(7);

    	monitoring_rules[random]={};
    	monitoring_rules[random]["as_name"]=as_name;
    	monitoring_rules[random]["monitor_id"]=monitor_id;
    	monitoring_rules[random]["filter"]=false;
    	var src_ip=as_monitor_info.match.ipv4_src.split(".")[3];
    	monitoring_rules[random]["src_ip"]=Number(src_ip);
	monitoring_rules[random]["can_block"]=false;
	
    	var markup = "<tr id='monitor-row-" + random +"'><td id='as-name-"+random+"'></td>"+
		     "<td><pre>" + JSON.stringify(as_monitor_info, undefined, 4) +"</pre></td>"+	
		     "<td id='status-"+ random +"'></td></tr>";
	row_ids[random]=as_monitor_info.match;
    	$("#table-monitor").append(markup);
	var row = document.getElementById('monitor-row-'+random);
	if (row.style.display == '') {
        	row.style.display = 'none';
	}

    	var timer = setInterval(function () {
        	if (Math.floor(Date.now() / 1000) > as_monitor_info.end_time) {
            		clearInterval(timer);
        	}
        	$.ajax({
            		url: BASE_URI + "get_monitor&as_name=" + as_name + "&monitor_id=" + monitor_id,
            		type: "GET",
            		error: function () {
	    			//var error_data={packet_count:"Not reachable",speed:"Not reachable"};
	    			var error_data={packet_count:"Not reachable",speed:0};
            			populateMonitoringValues(random, as_name, error_data, as_monitor_info);
            		},
            		success: function (result) {
				console.log(result);
				if (typeof result !== 'undefined') {
					var iii=0;
				}
                		var resultParsed = JSON.parse(result);
                		if (resultParsed.success) {
                    			populateMonitoringValues(random, as_name, resultParsed.data, as_monitor_info);
                		}
			},
                        timeout: 2000
        	});



        }, (parseInt(as_monitor_info.frequency) + 1) * 1000); 

    	//var auto_detection_times=setInterval(function() {
	//	auto_detection();	
	//}, (parseInt(as_monitor_info.frequency) + 2) * 1000);

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
								eth_type: 2048,
                        					tcp_src: 0,
                        					tcp_dst: 0,
                        					udp_src: 0,
                        					udp_dst: 0
	        		            		},
        	            				monitor_frequency: 1,
				                    	monitor_duration: 10000,
							priority: 60000
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







function get_messages(){
        $.ajax({
                url: BASE_URI + "get_messages",
                type: "GET",
                success: function (result) {
                        result=JSON.parse(result);
                        for (var key in result){
                                temp_row_id=row_id_map[key];
                                $("#message-" + temp_row_id).html(result[key]);
                        }

                }
        });
}


function update_amon(monitor_id,as_na,log_message, table_name){
        var data={id: monitor_id,message:log_message,as_name:as_na, table:table_name};
        $.ajax({
            url: BASE_URI + "update_amon",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: function (result) {
                console.log("Updated AMON"+monitor_id+" "+JSON.stringify(result));
            }
        });
}



function add_filter(match_array, matched_key){
	var data={matches: match_array};
        $.ajax({
            url: BASE_URI + "get_monitor_id_on_filter",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: function (result) {
		if(result.hasOwnProperty('hpc057')){
			delete result.hpc057;
		}
		//Check if the proxy connection is OK
		//markhere
		if (proxy_flag==0 && proxy_counter>=250){
			console.log("In proxy.. Sending message");
			$.ajax({
				url: BASE_URI + "send_proxy_info_amon",
				type: "POST",
				data: JSON.stringify(result),
				contentType: "application/json",
				dataType: "json",
				success: function (proxy_result) {
					proxy_flag=1;
					console.log("SENT TO PROXY");
					console.log(proxy_result);
					update_amon(0,result.as_name,"done", "AMON_SENSS");
				}
			});
		}
		else{
			for (var as_name in result) {
				var monitor_id=result[as_name];
				console.log("2CHECKING "+as_name+" "+as_name.localeCompare("hpc057"));
				$.ajax({
					url: BASE_URI + "add_filter&as_name=" + as_name + "&monitor_id=" + monitor_id,
					type: "GET",
		                	success: function (result) {
						filter_added_dict[as_name]=[];		
						result=JSON.parse(result);
						update_amon(0,result.as_name,"done", "AMON_SENSS");
						var row = document.getElementById('status-'+matched_key);
						filter_added_dict[as_name].push(matched_key);
						row.innerHTML="Filter added";
			                }	
				});
			}
		}

            }
        });
	
}


//Reads from AMON database
function get_amon_data(){
        $.ajax({
            url: BASE_URI + "get_amon_data",
            type: "GET",
            success: function (result) {
                        if (result.length!=0){
                                result=JSON.parse(result);	
                                total_rules=0;
				console.log(result);
                                for (var counter in result){
					var matches=[];
					var parse_array=JSON.parse(result[counter]["match_field"]);
					for (var key in row_ids){
						if (objectEquals(parse_array,row_ids[key])){
							var row = document.getElementById('monitor-row-'+key);
							if (row.style.display == 'none') {
        							row.style.display = '';
							}
							var row = document.getElementById('status-'+key);
							row.innerHTML="Filter obtained";
							var matched_key=key;
							var as_name=result[counter]["as_name"];
							filter_obtained_dict[as_name]=[];
							filter_obtained_dict[as_name].push(key);
						}
					}
					for (var key in parse_array) {
						matches.push(parse_array[key]);
					}
					                                                        
					setTimeout(function() {
						add_filter(matches, matched_key);
					}, 4000)
                                }
                        }
                        else{
                                console.log("Nothing present");
                        }
            }
        });
}

function check_reachability(){
	if (proxy_counter>proxy_threshold){
		var row = document.getElementById('proxy_tag');
		row.innerHTML="No";
		row.style.color="red";
		cy.$("#proxy_link").data("name", "Not reachable").style("line-color", "red");
		cy.$("#proxy").data("color", "yellow");
	}
	else{
		var row = document.getElementById('proxy_tag');
		row.innerHTML="Yes";
		row.style.color="green";
		cy.$("#proxy_link").data("name", "Reachable").style("line-color", "green");

	}
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


	random_nodes=["ANS","AT&T","LATNET","Cogent","PalmettoNet"];
	for(var as_name in sum_array){
		for(var r=1;r<=myConstClass.number_of_nodes;r++){
			if(random_nodes.indexOf(node_mapper[as_name+"_"+r])>-1){
			//if (random_nodes.indexOf(r)>-1){
	    			cy.$("#"+as_name+"_"+r).data("color","red");
			}else{
	    			cy.$("#"+as_name+"_"+r).data("color","gray");
			}
		}
		for(var r=0;r<random_nodes.length;r++){
			var ran=random_nodes[r];
		}
    	}

        var timer = setInterval(function () {
                get_amon_data();
        }, 3000);

        var timer = setInterval(function () {
                check_reachability();
        }, 500);

});

