$(document).ready(function(){
    //////// init ///////////
    $('#result').hide();
    
    function addCities(){
	    
	var div = $('<div class="form-group dests"><label class="col-sm-2"></label><div class="col-sm-10 text-left"></div></div>').insertAfter('div.dests:last');
	for(var i=0; i<3; i++){
	    $('div.dests:last .col-sm-10').append("<input class='dest form-control pull-left box'/>");
	};
    }
    // addCities();

    $('button#moreDest').on('click', function(e){
	addCities();
	e.preventDefault();
    });
    
    $("#startTime").add("#endTime").datepicker({
	dateFormat:'yy-mm-dd'
    });

    $.getJSON('/static/airports.json', function(data){
	var rows = $.map(data, function(row, index){
	    return {'label': row['city'] + '(' + row['name'] + ')',
		    'value': row['city']};
	});
		    
	$( ".dest" ).autocomplete({
	    source: rows
	});
    });
    
    $('button#search').on('click', function(e){
	var cities= $.map(
	    $('.dests input')
		.filter(function(){
		    return $(this).val().length > 0;
		}),
	    function(r){
		return $(r).val().toString();
	    });
	var post_data = {
	    'startTime': $('#startTime').val(),
	    'endTime': $('#endTime').val(),
	    'homeCity': 'Helsinki',
	    'cities': cities
	};
	console.log('post data:', post_data);
	console.log(JSON.stringify(post_data));
	$.ajax({
	    url: '/search',
	    type: 'POST',
	    contentType:'application/json',
	    data: JSON.stringify(post_data),
	    dataType:'json',
	    success: function(data){
		//On ajax success do this		
		var w = 1000;
		var h = 50 * (data['options'].length + 1); 
		var svg = d3.select('#result')
			.append('svg')
			.attr("width", w)
			.attr("height", h);
		console.log(data);
		plot_trips(svg, data['options']);
		$('#result').show();
	    },
	    error: function(xhr, ajaxOptions, thrownError) {
		//On error do this
		// $.mobile.loading('hide')
		if (xhr.status == 200) {
		    console.log(ajaxOptions);
		}
		else {
		    console.error(xhr.status);
		    console.error(thrownError);
		}
	    }
	});
	e.preventDefault();
    }).click();
});
