$(document).ready(function(){
    function addCities(){
	    
	var div = $('<div class="form-group dests"><label class="col-sm-2"></label><div class="col-sm-10 text-left"></div></div>').insertAfter('div.dests:last');
	for(var i=0; i<3; i++){
	    $('div.dests:last .col-sm-10').append("<input class='dest form-control pull-left box'/>");
	};
    }
    addCities();

    $('button#moreDest').on('click', function(e){
	addCities();
	e.preventDefault();
    });
    
    $("#startTime").add("#endTime").datepicker();

    $.getJSON('/static/airports.json', function(data){
	var rows = $.map(data, function(row, index){
	    return {'label': row['city'] + '(' + row['name'] + ')',
		    'value': row['code']};
	});
		    
	$( ".dest" ).autocomplete({
	    source: rows
	});
    });
    
});
