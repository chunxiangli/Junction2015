$(document).ready(function(){
    //////// init ///////////
    $('#result').hide();
    $('#partnerResult').hide();
    $('#loader').show();
    
    var airports = null;
    
    function addCities(){
	    
	var div = $('<div class="form-group dests"><label class="col-sm-2"></label><div class="col-sm-10 text-left"></div></div>').insertAfter('div.dests:last');
	for(var i=0; i<3; i++){
	    $('div.dests:last .col-sm-10').append("<input class='dest form-control pull-left box'/>");
	};
    }
    // addCities();

    $('button#moreDest').on('click', function(e){
	addCities();
	$( ".dest" ).autocomplete({
	    source: airports
	});
	e.preventDefault();
    });
    
    $("#startTime").add("#endTime").datepicker({
	dateFormat:'yy-mm-dd'
    });

    $.getJSON('/static/airports.json', function(data){
	airports = $.map(data, function(row, index){
	    return {'label': row['city'] + '(' + row['name'] + ')',
		    'value': row['city']};
	});
		    
	$( ".dest" ).autocomplete({
	    source: airports
	});
    });
    
    function getFormData(){
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
	return post_data;
    }
    var loader = $('#loader');
    $(document).ajaxStart(function(){
	loader.show();	
    });
    
    $('button#search').on('click', function(e){
	var post_data = getFormData();
	$.ajax({
	    url: '/search',
	    type: 'POST',
	    contentType:'application/json',
	    data: JSON.stringify(post_data),
	    dataType:'json',
	    success: function(data){
		//On ajax success do this		
		var w = 2000;
		var h = 50 * (data['options'].length + 1) + 50; 
		var svg_padding_left = 500;
		
		// clean stuff
		d3.select('svg').remove();
		
		var svg = d3.select('#result')
			.append('svg')
			.attr("width", w)
			.attr("height", h)
		plot_trips(svg, data['options']);
		$('#result').show();
		loader.hide();
	    },
	    error: function(xhr, ajaxOptions, thrownError) {
		if (xhr.status == 200) {
		    console.log(ajaxOptions);
		}
		else {
		    console.error(xhr.status);
		    console.error(thrownError);
		}
		loader.hide();
	    }
	});
	e.preventDefault();
    }).click();

    $("button#findPartner").on("click", function(e){
	var post_data = getFormData();
	$.ajax({
	    url: '/find',
	    type: 'POST',
	    contentType:'application/json',
	    data: JSON.stringify(post_data),
	    dataType:'json',
	    success: function(d){
		//On ajax success do this
		if(d['status'] == 0){
		    $.each(d['items'], function(i, item){
			$('ul.mate_list').append('<li>' + item + ' </li>');
		    });		    
		}
		else{
		    $('#partnerResult .lead').text(d['msg']);
		}
		$('#partnerResult').show();
		loader.hide();
	    },
	    error: function(xhr, ajaxOptions, thrownError) {
		if (xhr.status == 200) {
		    console.log(ajaxOptions);
		}
		else {
		    console.error(xhr.status);
		    console.error(thrownError);
		}
		loader.hide();
	    }
	});
	e.preventDefault();
    });
});

