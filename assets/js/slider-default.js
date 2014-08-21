$(function(){
	
	var currentValue = $('#currentValue');
	$('#defaultSlider').slider({value:[5, 10, 15, 100]});
	$('#defaultSlider').change(
		function(){
	    	currentValue.html(this.value);
	    	initialize();
		}
	);
	
	// Trigger the event on load, so
	// the value field is populated:
	$('#defaultSlider').change();
});

$(function(){
	
	var currentValue = $('#currentValue2');
	
	$('#defaultSlider2').change(
		function(){
	    	currentValue.html(this.value);
	    	initialize();
		}
	);
	
	// Trigger the event on load, so
	// the value field is populated:
	
	$('#defaultSlider2').change();
});

$('#defaultSlider').onMouseDown = function(){alert("5");};

function get_curr() {
	return $('#currentValue').html(this.value);
}

function get_curr2() {
	return $('#currentValue2').html(this.value);
}
