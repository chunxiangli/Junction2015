function plot_one_trip(trip){
    
}

function parse_datetime(str){
    var segs = str.split(" ");
    var dt = new Date(segs[0]);
    var hour = parseInt(segs[1].split(":")[0]);
    var minute = parseInt(segs[1].split(":")[1]);
    dt.setHours(hour);
    dt.setMinutes(minute);
    return dt;
}

function milisec2hour(t){
    console.log(t);
    return t / 1000 / 3600;
}

function scaled_position_of_time(start, end, t, length){
    //time inputs should be Date object
    console.log('end - start', end - start);
    console.log('t, start', t, start);
    console.log('t - start', t - start);
    var diff_hours_total = milisec2hour(end - start);
    var diff_hours_until_t = milisec2hour(t - start);
    // console.log(diff_hours_until_t, diff_hours_total);
    // console.log(length  * diff_hours_until_t / diff_hours_total);
    if(diff_hours_until_t == 0){
	return 0;
    }
    else{
	return length  * diff_hours_until_t / diff_hours_total;
    }
}

function time_anchors_between_period(start, end){
    //return 12:00am of all days between a period of time
    var cur_time = new Date(start);
    cur_time.setHours(12);
    cur_time.setMinutes(0);
    var ts = [];
    while(cur_time < end){
	ts.push(new Date(cur_time));
	cur_time.setDate(cur_time.getDate() + 1);
    }
    return ts;
}

function plot_trips(svg, data){
    var all_dts = [];
    $.each(data, function(i, row){
	$.each(row['trips'], function(i, trip){
	    trip['startTime'] = parse_datetime(trip['startTime']);
	    trip['endTime'] = parse_datetime(trip['endTime']);
	    all_dts.push(trip['startTime']);
	    all_dts.push(trip['endTime']);
	});
    });
    var min_dt = all_dts.reduce(function (a, b) { return a < b ? a : b; });
    var max_dt = all_dts.reduce(function (a, b) { return a > b ? a : b; });
    console.log('max_dt, min_dt:', min_dt, max_dt);
    $.each(data, function(i, row){
	$.each(row['trips'], function(trip, i){
	    trip['x1'] = scaled_position_of_time(min_dt, max_dt, trip['startTime'], svg.attr('width'));
	    trip['x2'] = scaled_position_of_time(min_dt, max_dt, trip['endTime'], svg.attr('width'));
	});
    });    
    
    $.each(data, function(i, row){
	svg.selectAll('rect')
	    .data(row['trips'])
	    .enter()
	    .append('rect')
	    .attr('fill', '#333')
	    .attr('width', function(t){
		console.log('x2-x1', t['x2'] - t['x1']);
		return t['x2'] - t['x1'];
	    })
	    .attr('x', function(t){
		return t['x1'];
	    });
    });
    
	
    // time_anchors_between_period();
}

$(document).ready(function(){
    $.getJSON("/static/example_trips_short.json", function(data){
	var w = 500;
	var h = 50; 
	var svg = d3.select('#content')
		.append('svg')
		.attr("width", w)
		.attr("height", h);
	console.log('plot_trips');
	plot_trips(svg, data['options']);
    });
});