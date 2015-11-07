$(document).ready(function(){
    for(var i=0; i<5; i++){
	$("#dests").append("<br/><input class='dest'>");
    };		

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
