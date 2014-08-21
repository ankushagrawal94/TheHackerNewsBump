$(function(){
	
	var slider = $('#slider'),
		min = slider.attr('min'),
		max = slider.attr('max'),
		currentValue = $('#currentValue');
	
	// Hiding the slider:
	slider.hide();
	
	$('#control').knobKnob({
		snap : 10,
		value: 250,
		turn : function(ratio){
			// Changing the value of the hidden slider
			slider.val(Math.round(ratio*(max-min) + min));
			
			// Updating the current value text
			currentValue.html(slider.val());
		}
	});
	
});
