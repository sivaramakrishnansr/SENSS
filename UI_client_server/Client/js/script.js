var thresholdRateMultiplier = 1;
var threshold = 0;

function populateMonitoringValues(rowId, as_name, data) {
    $("#packet-count-" + rowId).html(data.packet_count);
    $("#byte-count-" + rowId).html(data.byte_count);
    $("#speed-" + rowId).html(data.speed);
    if (parseInt(data.speed) >= threshold) {
        cy.$("#root_" + as_name).data("name", display_threshold(parseInt(data.speed))).style("line-color", "red");
    } else {
        cy.$("#root_" + as_name).data("name", display_threshold(parseInt(data.speed))).style("line-color", "green");
    }
}

function poll_stats(as_name, monitor_id, as_monitor_info) {
    var random = Math.random().toString(36).substring(7);
    var markup = "<tr id='monitor-row-" + random +"'><td>" + as_name + "</td><td><pre>" + JSON.stringify(as_monitor_info, undefined, 4) +
        "</pre></td><td id='packet-count-" + random + "'></td><td id='byte-count-" + random + "'>" +
        "</td><td id='speed-" + random + "'></td><td><p><button type='button' class='btn btn-default' " +
        "id='remove-monitor-" + random + "'>Remove Monitor</button></p><p><button type='button' class='btn btn-success' " +
        "id='add-filter-" + random + "'>Add Filter</button></p><p><button type='button' class='btn btn-danger' " +
        "id='remove-filter-" + random + "'>Remove Filter</button></p></td></tr>";
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
            success: function (result) {
                var resultParsed = JSON.parse(result);
                if (resultParsed.success) {
                    populateMonitoringValues(random, as_name, resultParsed.data);
                }
            }
        });
    }, (parseInt(as_monitor_info.frequency) + 2) * 1000); // rule[2] is actual frequency with which the backend system will update the database/
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
        return (int_threshold / Math.pow(10, 12)).toString() + " TBps";
    } else if (zeros >= 9) {
        return (int_threshold / Math.pow(10, 9)).toString() + " GBps";
    } else if (zeros >= 6) {
        return (int_threshold / Math.pow(10, 6)).toString() + " MBps";
    } else if (zeros >= 3) {
        return (int_threshold / Math.pow(10, 3)).toString() + " KBps";
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
