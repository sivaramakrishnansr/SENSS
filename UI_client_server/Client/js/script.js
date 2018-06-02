var thresholdRateMultiplier = 1;
var threshold = 0;
var proxy_counter = 0;
var proxy_flag=0;
var sum_array={"hpc039":0,"hpc041":0,"hpc042":0,"hpc043":0,"hpc044":0,"hpc046":0,"hpc047":0,"hpc048":0,"hpc049":0,"hpc050":0,"hpc052":0,"hpc054":0,"hpc056":0,"hpc057":0}

function populateMonitoringValues(rowId, as_name, data) {
    if (data.speed=="Not reachable"){
	    sum_array[as_name]=0;
	    $("#packet-count-" + rowId).html("N/A");
    	    //$("#byte-count-" + rowId).html(data.byte_count);
            //$("#speed-" + rowId).html(data.speed);
    	    $("#speed-" + rowId).html("N/A");
            cy.$("#root_" + as_name).data("name", "N/A").style("line-color", "#996300");
	proxy_counter=proxy_counter+1;
	if (proxy_counter==5)
	{
		if (proxy_flag==0){
			proxy_flag=1;
	        $.ajax({
		 url: BASE_URI + "send_proxy_info",
            	 type: "GET",
           	 success: function (result) {
			console.log("Sent information to proxy");
	            }
        	});
		}
	}

    }

    else{
	sum_array[as_name]=data.speed;
    	$("#packet-count-" + rowId).html(data.packet_count);
    	//$("#byte-count-" + rowId).html(data.byte_count);
    	//$("#speed-" + rowId).html(data.speed);
    	$("#speed-" + rowId).html(display_threshold(data.speed));
    	if (parseInt(data.speed) >= threshold) {
        	cy.$("#root_" + as_name).data("name", display_threshold(parseInt(data.speed))).style("line-color", "red");
    	} else {
        	cy.$("#root_" + as_name).data("name", display_threshold(parseInt(data.speed))).style("line-color", "green");
    	}
    }
    var all_speed=0;
    for (var key in sum_array){
		all_speed=all_speed+Number(sum_array[key]);
	}
    $("#all_speed").html(display_threshold(all_speed));
    console.log("Speed "+all_speed);
}

function poll_stats(as_name, monitor_id, as_monitor_info) {
    var random = Math.random().toString(36).substring(7);
    var markup = "<tr id='monitor-row-" + random +"'><td>" + as_name + "</td><td><pre>" + JSON.stringify(as_monitor_info, undefined, 4) +
        "</pre></td><td id='packet-count-" + random + "'></td>"+
	//"<td id='byte-count-" + random + "'>" +"</td>"
	"<td id='speed-" + random + "'></td></tr>"
	//<td><p><button type='button' class='btn btn-default' " ;
	//+
        //"id='remove-monitor-" + random + "'>Remove Monitor</button></p><p><button type='button' class='btn btn-success' " +
        //"id='add-filter-" + random + "'>Add Filter</button></p><p><button type='button' class='btn btn-danger' " +
        //"id='remove-filter-" + random + "'>Remove Filter</button></p></td></tr>";
    $("#table-monitor").append(markup);

    $("#remove-filter-" + random).hide();

    var timer = setInterval(function () {
        if (Math.floor(Date.now() / 1000) > as_monitor_info.end_time) {
            clearInterval(timer);
        }
	console.log(BASE_URI + "get_monitor&as_name=" + as_name + "&monitor_id=" + monitor_id);
        $.ajax({
            url: BASE_URI + "get_monitor&as_name=" + as_name + "&monitor_id=" + monitor_id,
            type: "GET",
            error: function () {
	    	var error_data={packet_count:"Not reachable",speed:"Not reachable"};
            	populateMonitoringValues(random, as_name, error_data);
            },
            success: function (result) {
		if (typeof result !== 'undefined') {
			console.log(result);
		}
                var resultParsed = JSON.parse(result);
                if (resultParsed.success) {
                    populateMonitoringValues(random, as_name, resultParsed.data);
                }
            },
	    timeout: 2000
        });
    }, (parseInt(as_monitor_info.frequency) + 2) * 1000); 
    //}, (parseInt(as_monitor_info.frequency)) * 1000); 
    // rule[2] is actual frequency with which the backend system will update the database/
    // We give couple more seconds to reflect the data in the DB and then fetch the updated data.

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
    $("#current-threshold").html(display_threshold(threshold));
}

$(document).ready(function () {
    set_threshold();
    $("#add-monitoring-rule").click(function () {
        $("#add-monitor-modal").modal('show');
    });

    $("#add-filter-all").click(function () {
	    var xhttp = new XMLHttpRequest();
    	    xhttp.open("GET", BASE_URI+"add_filter_all", true);
            xhttp.setRequestHeader("Content-type", "application/json");
            xhttp.send();
    });

    $("#remove-filter-all").click(function () {
	    var xhttp = new XMLHttpRequest();
    	    xhttp.open("GET", BASE_URI+"remove_filter_all", true);
            xhttp.setRequestHeader("Content-type", "application/json");
            xhttp.send();
    });

	
    
    $("#add-monitor-rule").click(function () {
        var data = {
            as_name: $("#as_name").val(),
            match: {
                nw_src: $("#nw_src").val(),
                nw_dst: $("#nw_dst").val(),
                tcp_src: $("#tcp_src").val(),
                tcp_dst: $("#tcp_dst").val(),
                udp_src: $("#udp_src").val(),
                udp_dst: $("#udp_dst").val()
            },
            monitor_frequency: parseInt($("#monitor_freq").val()),
            monitor_duration: parseInt($("#monitor_duration").val())
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
                $('#add-monitor-modal').modal('toggle');
            }
        });
    });

    $("#set-threshold").click(function () {
        $("#set-threshold-modal").modal('show');
    });

    $('.dropdown-menu a').click(function () {
        var rate = $(this).text();
        $('#selected').text(rate);
        if (rate == "KBps") {
            thresholdRateMultiplier = 1000;
        } else if (rate == "MBps") {
            thresholdRateMultiplier = 1000 * 1000;
        } else if (rate == "GBps") {
            thresholdRateMultiplier = 1000 * 1000 * 1000;
        } else if (rate == "TBps") {
            thresholdRateMultiplier = 1000 * 1000 * 1000 * 1000;
        }
    });

    $("#set-threshold-button").click(function () {
        var value = parseInt($("#threshold-value").val());
        threshold = value * thresholdRateMultiplier;
        localStorage.setItem("threshold", threshold);
        $("#current-threshold").html(display_threshold(threshold));
        $("#set-threshold-modal").modal('hide');
    });
});
