BASE_URI = "api.php?action=";
var thresholdRateMultiplier = 1;
var threshold = 10;



function populateMonitoringValues(data,rowId,match) {
        $("#as-name-" + rowId).html(data.as_name);
        $("#request-type-" + rowId).html(data.request_type);
        $("#match-" + rowId).html(data.match_field);
        $("#request-count-" + rowId).html(data.count_request_type);
}

function poll_stats() {
        var check_random=[];
        var timer = setInterval(function () {
                $.ajax({
                        url: BASE_URI + "get_server_logs",
                        type: "GET",
                        success: function (result) {
                                var resultParsed = JSON.parse(result);
                                if (resultParsed.success) {
                                        for (var i = 0; i < resultParsed.data.length; i++) {
                                                 var random = resultParsed.data[i].as_name+"_"+resultParsed.data[i].request_type.replace(/\s/g, '');
                                                 if (check_random.indexOf(random)==-1){
                                                        check_random.push(random);
                                                         var markup = "<tr id='monitor-row-" + random +"'>" +
                                                                "<td id='as-name-" + random + "'></td>" +
                                                                "<td id='request-type-" + random + "'></td>" +
                                                                "<td id='match-" + random + "'><pre></pre></td>" +
                                                                "<td id='request-count-" + random + "'><pre></pre></td>";
                                                        $("#table-monitor").append(markup);
                                                }
                                                populateMonitoringValues(resultParsed.data[i],random);
                                        }
                                }
                        }
                });
        }, (1* 1000)); // rule[2] is actual frequency with which the backend system will update the database/
}

function set_threshold() {
        var storedThreshold = localStorage.getItem("threshold");
        if (storedThreshold != null) {
                threshold = parseInt(storedThreshold);
        }
        $("#current-threshold").html(threshold+" Rules");
}

function get_controller_url(){
	console.log("Getting controller url");
	$.ajax({
		url: "api.php?get_controller",
		success: function (result) {
			console.log("SIVARAM: Added rules",result);
			 $("#controller_url_placeholder").html(result);
		}
	});	
}

$(document).ready(function () {
        set_threshold();
        poll_stats();
	get_controller_url();
        $("#set-threshold").click(function () {
                $("#set-threshold-modal").modal('show');
        });

        $("#add-controller").click(function () {
                $("#add-controller-modal").modal('show');
        });


        $("#set-threshold-button").click(function () {
                var value = parseInt($("#threshold-value").val());
                threshold=value;
                localStorage.setItem("threshold", threshold);
                $("#current-threshold").html(threshold+" Rules");
                $("#set-threshold-modal").modal('hide');
                $.ajax({
                        type: "POST",
                        url: 'threshold.php',
                        dataType: 'json',
                        data: {functionname: 'insert_threshold', arguments: [threshold]},
                        success: function (result) {
                                console.log("Inserted"+result);
                        }
                });
         });


        $("#add-controller-button").click(function () {
                        var controller_url = $("#controller_url").val();
                        var data={"controller_url":controller_url};
                        console.log("Data",data);
                        $.ajax({
                                url: "api.php?add_controller",
                                type: "POST",
                                data: JSON.stringify(data),
                                contentType: "application/json",
                                dataType: "json",
                                success: function (result) {
                                        console.log("SIVARAM: Added rules");
                                }
                        });
                        $("#add-controller-modal").modal('hide');
                        location.reload();
        });


});

