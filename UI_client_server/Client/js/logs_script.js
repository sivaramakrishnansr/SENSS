BASE_URI = "api.php?";
var thresholdRateMultiplier = 1;
var threshold = 0;




function poll_stats() {
        var check_random=[];

		var add_monitor={};
                $.ajax({
                        url: BASE_URI + "get_client_logs&type=add_monitor",
                        type: "GET",
                        success: function (result) {
                                var resultParsed = JSON.parse(result);
                                if (resultParsed.success) {
                                        for (var i = 0; i < resultParsed.data.length; i++) {
						var random = Math.random().toString(36).substring(7);
                                                 if (check_random.indexOf(random)==-1){
                                                        check_random.push(random);
                                                }
						var as_name=resultParsed.data[i].as_name;
						var match_field=resultParsed.data[i].match_field;
						var time=resultParsed.data[i].time;
						if (!(as_name in add_monitor)){
							add_monitor[as_name]=[];
						}
						add_monitor[as_name].push([match_field,time]);
                                        }
                                }
				var markup="<div class='container inner-container'><a data-toggle='collapse' data-target='#monitoring_rules'><h2>Monitoring rules</h2></a><div id='monitoring_rules'>";
				for (const [ key, value ] of Object.entries(add_monitor)) {
					console.log(key);
					markup=markup+"<h3>"+key+"</h3><table class='table table-bordered table-striped'><thead><tr><th>Time</th><th>Match</th></tr></thead>";
					for (var i=0;i< add_monitor[key].length; i++){
                                                         markup =markup+ "<tr>" +
                                                                "<td>"+add_monitor[key][i][1]+"</td>" +
                                                                "<td><pre>"+JSON.stringify(JSON.parse(add_monitor[key][i][0]), undefined, 4)+"</pre></td></tr>"; 
						}
					
					markup=markup+"</table>";
				}
				markup=markup+"</div></div>";
                                $("#table-add-monitor").append(markup);


                        }
                });


		var monitor_stats={};
                $.ajax({
                        url: BASE_URI + "get_client_logs&type=monitor_stats",
                        type: "GET",
                        success: function (result) {
                                var resultParsed = JSON.parse(result);
                                if (resultParsed.success) {
                                        for (var i = 0; i < resultParsed.data.length; i++) {
						var random = Math.random().toString(36).substring(7);
                                                 if (check_random.indexOf(random)==-1){
                                                        check_random.push(random);
                                                }
						var as_name=resultParsed.data[i].as_name;
						var speed=resultParsed.data[i].speed;
						var time=resultParsed.data[i].time;
						if (!(as_name in monitor_stats)){
							monitor_stats[as_name]=[];
						}
						monitor_stats[as_name].push([speed,time]);
                                        }
                                }
				var markup="<div class='container inner-container'><a data-toggle='collapse' data-target='#monitoring_stats'><h2> Monitoring stats</h2></a><div id='monitoring_stats'>";
				for (const [ key, value ] of Object.entries(monitor_stats)) {
					console.log(key);
					markup=markup+"<h3>"+key+"</h3><table class='table table-bordered table-striped'><thead><tr><th>Time</th><th>Speed</th></tr></thead>";
					for (var i=0;i< monitor_stats[key].length; i++){
                                                         markup =markup+ "<tr>" +
                                                                "<td>"+monitor_stats[key][i][1]+"</td>" +
                                                                "<td>"+monitor_stats[key][i][0]+"</td></tr>"; 
						}

				markup=markup+"</table>";
				}
				markup=markup+"</div></div>";
                                $("#table-add-monitor").append(markup);

                        }
                });

		var filter_stats={};
                $.ajax({
                        url: BASE_URI + "get_client_logs&type=add_filter",
                        type: "GET",
                        success: function (result) {
                                var resultParsed = JSON.parse(result);
                                if (resultParsed.success) {
                                        for (var i = 0; i < resultParsed.data.length; i++) {
						var random = Math.random().toString(36).substring(7);
                                                 if (check_random.indexOf(random)==-1){
                                                        check_random.push(random);
                                                }
						var as_name=resultParsed.data[i].as_name;
						var time=resultParsed.data[i].time;
						if (!(as_name in filter_stats)){
							filter_stats[as_name]=[];
						}
						filter_stats[as_name].push([time]);
                                        }
                                }
				var markup="<div class='container inner-container'><a data-toggle='collapse' data-target='#filtering_stats'><h2>Filtering rules</h2></a><div id='filtering_stats'>";
				for (const [ key, value ] of Object.entries(filter_stats)) {
					console.log(key);
					markup=markup+"<h3>"+key+"</h3><table class='table table-bordered table-striped'><thead><tr><th>Time</th></tr></thead>";
					for (var i=0;i< filter_stats[key].length; i++){
                                                         markup =markup+ "<tr>" +
                                                                "<td>"+filter_stats[key][i][0]+"</td></tr>"; 
						}

				markup=markup+"</table>";
				}
				markup=markup+"</div></div>";
                                $("#table-add-monitor").append(markup);

                        }
                });


}


$(document).ready(function () {
        poll_stats();
});

