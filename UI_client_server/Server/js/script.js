BASE_URI = "api.php?action=";
var thresholdRateMultiplier = 1;
var threshold = 0;



function populateMonitoringValues(data,rowId,match) {
    $("#as-name-" + rowId).html(data.an_name);
    $("#request-type-" + rowId).html(data.request_type);
    $("#match-" + rowId).html(data.match_field);
    $("#packet-count-" + rowId).html(data.packet_count);
    $("#byte-count-" + rowId).html(data.byte_count);
    $("#speed-" + rowId).html(data.speed);
}

function poll_stats() {



   // var timer = setInterval(function () {
	    console.log(BASE_URI + "get_server_logs");

        $.ajax({
            url: BASE_URI + "get_server_logs",
            type: "GET",
            success: function (result) {
	        var resultParsed = JSON.parse(result);
        	        if (resultParsed.success) {
				console.log(resultParsed.data);
				for (var i = 0; i < resultParsed.data.length; i++) {
					 console.log(resultParsed.data[i]);
					 var random = Math.random().toString(36).substring(7);
    					 var markup = "<tr id='monitor-row-" + random +"'>" +
    						"<td id='as-name-" + random + "'></td>" +
    						"<td id='request-type-" + random + "'></td>" +
    						"<td id='match-" + random + "'><pre></pre></td>" +
    						"<td id='packet-count-" + random + "'></td>" +
						//"<td id='byte-count-" + random + "'></td>" +
    	        				"<td id='speed-" + random + "'></td></tr>";
    					 $("#table-monitor").append(markup);

                	   		 populateMonitoringValues(resultParsed.data[i],random);

				}
			}
            }
        });
    //}, (1 * 1000)); // rule[2] is actual frequency with which the backend system will update the database/
    // We give couple more seconds to reflect the data in the DB and then fetch the updated data.

}

function set_threshold() {
    var storedThreshold = localStorage.getItem("threshold");
    if (storedThreshold != null) {
        threshold = parseInt(storedThreshold);
    }
    //$("#current-threshold").html(display_threshold(threshold));
    $("#current-threshold").html(threshold+" Rules");
}

$(document).ready(function () {
set_threshold();
poll_stats();
    $("#set-threshold").click(function () {
        $("#set-threshold-modal").modal('show');
    });

    $("#set-threshold-button").click(function () {
        var value = parseInt($("#threshold-value").val());
        threshold=value;
        localStorage.setItem("threshold", threshold);
        $("#current-threshold").html(threshold+" Rules");
        $("#set-threshold-modal").modal('hide');
    });

});
