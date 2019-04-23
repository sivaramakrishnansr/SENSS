var threshold = 0;
var sum_array={"hpc039":{},"hpc041":{},"hpc042":{},"hpc043":{},"hpc044":{},"hpc046":{},"hpc047":{},"hpc048":{},"hpc049":{},"hpc050":{},"hpc052":{},"hpc054":{},"hpc056":{},"hpc057":{}}
var row_id_map={}
var monitor_ids={};
var global_speed=0;
var monitor_ids_available=false;

//Populating current traffic rate at the client
function populateMonitoringValues(rowId, as_name, data, display_flag) {
	row_id_map[as_name]=rowId;
	if (data=="SENSS not connected"){
		$("#speed-" + rowId).html("Connection to SENSS \n server not established");
		return;
	}
	if (display_flag==1){
		console.log("DATA "+JSON.stringify(data));
	}
	if (!(rowId in sum_array[as_name])){
        	sum_array[as_name][rowId]=0;
	}
	if (display_flag==0){
		sum_array[as_name][rowId]=data.speed;
	}
	var as_speed=0;
	for (var key in sum_array[as_name]){
        	as_speed=as_speed+Number(sum_array[as_name][key]);
	}
	if (parseInt(data.speed) >= 35*1000*1000*1000) {
        	cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "red");
       	} else {
        	cy.$("#root_" + as_name).data("name", display_threshold(parseInt(as_speed))).style("line-color", "green");
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

function filter(as_name,monitor_id){
        var data = {"as_name":as_name};
        $.ajax({
                url: BASE_URI + "get_monitor_status&as_name=" + as_name,
                type: "GET",
                success: function (result) {
                        if (result=="None"){
                                $.ajax({
                                        url: BASE_URI + "add_filter_alpha",
                                        type: "POST",
                                        data: JSON.stringify(data),
                                        contentType: "application/json",
                                        dataType: "json",
                                        success: function (result) {
                                                console.log("SENSS: Added rules "+as_name);
                                        }
                                });
                        }
                }
        });
}

//Polls the SENSS servers for traffic rates on flows based on monitoring rules which are added
function poll_stats(as_name, monitor_id, as_monitor_info, display_flag) {
	if (display_flag==1){
	        var random = Math.random().toString(36).substring(7);
        	var markup = "<tr id='monitor-row-" + random +"'><td>" + as_name + "</td><td><pre>" + JSON.stringify(as_monitor_info, undefined, 4) +
	        "</pre></td><td id='message-" + random + "'>Filter obtained</td></tr>";
	        $("#table-monitor").append(markup);
        	$("#remove-filter-" + random).hide();
	}
        //Polling is done for the specified limit
        //When the request suceeds, the packet counts and traffic rates are updated
        //The current packet counts and traffic rates are sent to populateMOnitoringValues
        var timer = setInterval(function () {
                if (Math.floor(Date.now() / 1000) > as_monitor_info.end_time) {
                        clearInterval(timer);
                }
                $.ajax({
                        url: BASE_URI + "get_monitor&as_name=" + as_name + "&monitor_id=" + monitor_id,
                        type: "GET",
                        error: function () {
				console.log("Request timed out. Attempting Again..");
                        },
                        success: function (result) {
				try{
	                        	var resultParsed = JSON.parse(result);
        	                	if (resultParsed.success) {
                	                	populateMonitoringValues(random, as_name, resultParsed.data,display_flag);				
                        		}
				}
				catch{
                	                	populateMonitoringValues(random, as_name, "SENSS not connected",display_flag);				

				}
                },
                 timeout: 2000
                });
        }, (parseInt(as_monitor_info.frequency) + 2) * 1000);


        //Removes the monitoring rule when the SENSS client user clicks on the Remove Monitor button
        $("#remove-monitor-" + random).click(function () {
                $.ajax({
                        url: BASE_URI + "remove_monitor&as_name=" + as_name + "&monitor_id=" + monitor_id,
                        type: "GET",
                        success: function (result) {
                                clearInterval(timer);
                                $("#monitor-row-" + random).remove();
                        }
                });
        });

        //Adds a traffic filter when the SENSS client user clicks on Add Filter button
        $("#add-filter-" + random).click(function () {
                $.ajax({
                url: BASE_URI + "add_filter&as_name=" + as_name + "&monitor_id=" + monitor_id,
                type: "GET",
                success: function (result) {
                        $("#add-filter-" + random).hide();
                        $("#remove-filter-" + random).show();
                }
                });
        });

        //Removes a traffic filter when the SENSS client user clicks on the Remove Filter button
        $("#remove-filter-" + random).click(function () {
                $.ajax({
                url: BASE_URI + "remove_filter&as_name=" + as_name + "&monitor_id=" + monitor_id,
                type: "GET",
                success: function (result) {
                        $("#add-filter-" + random).show();
                        $("#remove-filter-" + random).hide();
                }
                });
        });
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

//Checks if there are existing monitoring rules set by the SENSS client
function get_monitor_ids(){
        $.ajax({
            url: BASE_URI + "get_monitor_ids",
            type: "GET",
            success: function (result) {
                        monitor_ids=JSON.parse(result);
                        monitor_ids_available=true;
            }
        });
}

function add_filter(as_name,monitor_id){
	$.ajax({
		url: BASE_URI + "add_filter&as_name=" + as_name + "&monitor_id=" + monitor_id,
		type: "GET",
		success: function (result) {
			console.log("Added filter");
		}	
	});
}



function get_messages(){
	console.log("Getting messages");
	$.ajax({
		url: BASE_URI + "get_messages",
		type: "GET",
		success: function (result) {
			console.log("MEssages ",JSON.stringify(result));
			result=JSON.parse(result);
			for (var key in result){
				console.log("Got the message rules "+key+" "+result[key]);
				temp_row_id=row_id_map[key];
				$("#message-" + temp_row_id).html(result[key]);
			}

		}	
	});
}



function update_amon(monitor_id,as_na,log_message, table_name){
	console.log("Updated AMON");
	var data={id: monitor_id,message:log_message,as_name:as_na, table:table_name};
        $.ajax({
            url: BASE_URI + "update_amon",
            type: "POST",
	    data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: function (result) {
		console.log("Updated "+monitor_id+" "+JSON.stringify(result));
            }
        });
}


function add_rules(as_name,as_data, visible, message_id){
		console.log("Adding rules "+JSON.stringify(as_data));
        		$.ajax({
                		url: BASE_URI + "add_monitor",
	                	type: "POST",
        	        	data: JSON.stringify(as_data),
                		contentType: "application/json",
                		dataType: "json",
	                	success: function (result) {
        	                	result.as_name_id.forEach(function (as_name_id) {
                	        		poll_stats(as_name_id.as_name, as_name_id.monitor_id, result.match, visible);
						if (visible==1){
							update_amon(as_name_id.monitor_id,as_name_id.as_name,"Filter obtained","MONITORING_RULES");
							console.log("Added the rules "+JSON.stringify(result));
							setTimeout(function() {
							    add_filter(as_name_id.as_name,as_name_id.monitor_id);
							}, 4000)
							update_amon(as_name_id.monitor_id,as_name_id.as_name,"Added filter","MONITORING_RULES");
							update_amon(as_name_id.monitor_id,as_name_id.as_name,"Added filter","AMON_SENSS");
						}
                        		});
	                	},
        	                error: function (xhr, status, error) {
					console.log("ERROR "+xhr.responseText);
                        	}
	                });
}

function initial_rule_add(){
        $.ajax({
            url: BASE_URI + "get_monitor_ids",
            type: "GET",
            success: function (result) {
			if (result.length!=0){
				result=JSON.parse(result);
				total_rules=0;
				for (var key in result){
					console.log("Got the monitoring rules "+key+" "+result[key]);
					total_rules++;
				}
				if (total_rules==0){
					add_rules();
					var as_names=["hpc050","hpc052","hpc054","hpc056"]
					for (var i = 0; i < as_names.length; i++) {
						console.log("Adding rules for as_name "+as_names[i]);
				               	var data = {
			        	        	as_name: [as_names[i]],
			                		match: {
			                        		"ipv4_dst": "57.0.0.1",
								"eth_type": 2048
			        	        	},
			                		monitor_frequency: 1,
			                		monitor_duration: 1000,
							monitor_type: "init",
							priority: 11111
				        	};
						add_rules(as_names[i],data,0);
					}
				}
				else{
					console.log("Rules already present");
				}
				
			}
            }
        });
	
}

function get_amon_data(){
	console.log("Getting AMON data");
        $.ajax({
            url: BASE_URI + "get_amon_data",
            type: "GET",
            success: function (result) {
			if (result.length!=0){
				result=JSON.parse(result);
				total_rules=0;
				for (var counter in result){
					console.log("ID "+result[counter]["id"]);
					console.log("AS name "+result[counter]["as_name"]);
					console.log("Match field "+result[counter]["match_field"]);
					console.log("Frequency "+result[counter]["frequency"]);
					console.log("Monitor duration "+result[counter]["monitor_duration"]);
					console.log("AS Name "+result[counter]["as_name"]);
					total_rules++;
				        var data = {
			        	        	as_name: [result[counter]["as_name"]],
			                		match: JSON.parse(result[counter]["match_field"]),
			                		monitor_frequency: result[counter]["frequency"],
			                		monitor_duration: result[counter]["monitor_duration"],
							monitor_type: "user",
							priority: 60000
				      	};
					add_rules(result[counter]["as_name"],data,1,result[counter]["id"]);
				}
			}
			else{
				console.log("Nothing present");
			}
            }
        });
}


$(document).ready(function () {
	get_messages();
	initial_rule_add();
        //set_threshold();
        $("#add-monitoring-rule").click(function () {
                $("#add-monitor-modal").modal('show');
        });

        //Adds all filters when the SENSS client user clicks on the Add Filter All button
        $("#add-filter-all").click(function () {
                var xhttp = new XMLHttpRequest();
                xhttp.open("GET", BASE_URI+"add_filter_all", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send();
        });

        //Removes all filters when the SENSS client user clicks on the Remove Filter All button
        $("#remove-filter-all").click(function () {
                var xhttp = new XMLHttpRequest();
                xhttp.open("GET", BASE_URI+"remove_filter_all", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send();
        });

        //Obtaines flow level information for adding monitoring rules
        $("#add-monitor-rule").click(function () {
                var data = {
                	as_name: $("#as_name").val(),
                	match: {
                        	ipv4_src: $("#nw_src").val(),
                        	ipv4_dst: $("#nw_dst").val(),
                        	tcp_src: $("#tcp_src").val(),
                        	tcp_dst: $("#tcp_dst").val(),
                        	udp_src: $("#udp_src").val(),
                        	udp_dst: $("#udp_dst").val()
                	},
                	monitor_frequency: parseInt($("#monitor_freq").val()),
                	monitor_duration: parseInt($("#monitor_duration").val()),
			monitor_type: "user"
        	};
        	$.ajax({
                	url: BASE_URI + "add_monitor",
                	type: "POST",
                	data: JSON.stringify(data),
                	contentType: "application/json",
                	dataType: "json",
                	success: function (result) {
                        	result.as_name_id.forEach(function (as_name_id) {
	                        	poll_stats(as_name_id.as_name, as_name_id.monitor_id, result.match, 1);
                        	});
                		$('#add-monitor-modal').modal('toggle');
                	},
                        error: function (xhr, status, error) {
				console.log("ERROR "+xhr.responseText);
                        }

                });
        });



    $("#set-threshold").click(function () {
        $("#set-threshold-modal").modal('show');
    });


    $("#set-threshold-button").click(function () {
        var value = parseInt($("#threshold-value").val());
        threshold=value;
        localStorage.setItem("threshold", threshold);
        $("#current-threshold").html(threshold+"%");
        $("#set-threshold-modal").modal('hide');
    });

        var timer = setInterval(function () {
		get_amon_data();
        }, 1000);

        var timer = setInterval(function () {
		get_messages();
        }, 100);

});
