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
    // console.log(t);
    return t / 1000 / 3600;
}

function scaled_position_of_time(start, end, t, length){
    //time inputs should be Date object
    // console.log('end - start', end - start);
    // console.log('t, start', t, start);
    // console.log('t - start', t - start);
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
    var W = parseInt(svg.attr('width'));
    var H = parseInt(svg.attr('height'));
    
    $.each(data, function(row_i, row){
	row['id'] = row_i
	$.each(row['trips'], function(i, trip){
	    trip['startTime'] = parse_datetime(trip['startTime']);
	    trip['endTime'] = parse_datetime(trip['endTime']);
	    trip['row'] = row_i;
	    all_dts.push(trip['startTime']);
	    all_dts.push(trip['endTime']);
	});
    });
    var min_dt = all_dts.reduce(function (a, b) { return a < b ? a : b; });
    var max_dt = all_dts.reduce(function (a, b) { return a > b ? a : b; });
    // console.log('max_dt, min_dt:', min_dt, max_dt);
    $.each(data, function(i, row){
	$.each(row['trips'], function(i, trip){
	    // console.log(min_dt, max_dt, trip['startTime'], trip['endTime'],
	    // 		scaled_position_of_time(min_dt, max_dt, trip['startTime'], W),
	    // 	       scaled_position_of_time(min_dt, max_dt, trip['endTime'], W));
	    trip['x1'] = scaled_position_of_time(min_dt, max_dt, trip['startTime'], W);
	    trip['x2'] = scaled_position_of_time(min_dt, max_dt, trip['endTime'], W);
	});
    });

    // add trip events
    var rec_h = 50;
    svg
	.selectAll('g')
	.data(data)
	.enter()
	.append('g')
	.attr('fill', function(d, i){
	    if(i % 2){
		return '#E5F4FC';
	    }
	    else{
		return '#ffffff';
	    }
	})
	.selectAll('rect')
	.data(function(d, i){
	    return d['trips'];
	})
	.enter()
	.append('rect')
	.attr('fill', '#888')
	.attr('height', rec_h)
	.attr('width', function(t){
	    return t['x2'] - t['x1'];
	})
	.attr('x', function(t){
	    return t['x1'];
	})
    	.attr('y', function(t, i){
	    var paddingTop = 40;
	    if(t['row']==0){
		return paddingTop;
	    }
	    else{
		return paddingTop + rec_h * t['row'];
	    }
	});
    
	
    // add anchor date text
    var anchor_dts = time_anchors_between_period(min_dt, max_dt);
    var anchor_pts = $.map(anchor_dts, function(dt){
	return {
	    'dt': dt.getMonth() + '-' + dt.getDate() + ' ' + dt.getHours() + 'am',
	    'x': scaled_position_of_time(min_dt, max_dt, dt, W)
	};
    });
    
    svg.append('g')
	.selectAll('text')
	.data(anchor_pts)
	.enter()
	.append('text')
	.attr('y', 30)
	.attr('x', function(pt){
	    return pt['x'] - 25;
	})
	.text(function(pt){
	    return pt['dt'];
	});
    // add anchor date vertical line
    svg.append('g')
	.selectAll('line')
	.data(anchor_pts)
	.enter()
	.append('line')
	.attr('x1', function(pt){
	    return pt['x'];
	})
	.attr('x2', function(pt){
	    return pt['x'];
	})
	.attr('y1', 33)
	.attr('y2', H)
	.attr('stroke', '#eee')
	.attr('stroke-width', 1);
}

$(document).ready(function(){
    $.getJSON("/static/example_trips.json", function(data){
	var w = 1000;
	var h = 50 * (data['options'].length + 1); 
	var svg = d3.select('#content')
		.append('svg')
		.attr("width", w)
		.attr("height", h);
;
	plot_trips(svg, data['options']);
    });
});

function test(svg){
    svg.selectAll('rect')
	.data([1, 2, 3])
	.enter()
	.append('rect')
	.attr('width', 50)
	.attr('height', 10)
	.attr('x', function(x){
	    console.log(x);
	    return x * 100;
	})
	.attr('fill', '#666');

}