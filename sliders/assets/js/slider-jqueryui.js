/*$(function(){
	
	var currentValue = $('#currentValue');

	$("#slider").slider({ 
		values: [0, 10, 15, 30],
		slide: function(event, ui) {
			currentValue.html(ui.value);
		}
	});
	
});*/


$(function() {
    var trueValues = [0, 500, 750, 1000, 1250, 1500, 2000, 2500, 75000, 100000, 150000, 200000, 250000, 300000, 350000, 400000, 500000, 1000000];
    var values =     [0,   1,   2,    3,    4,    5,    6,    7,    10,     15,     20,     25,     30,     40,     50,     60,     75,     100];
    var slider = $("#slider").slider({
        orientation: 'horizontal',
        range: true,
        min: 0,
        max: 100,
        values: [100],
        slide: function(event, ui) {
            var includeLeft = event.keyCode != $.ui.keyCode.RIGHT;
            var includeRight = event.keyCode != $.ui.keyCode.LEFT;
            var value = findNearest(includeLeft, includeRight, ui.value);
            if (ui.value == ui.values[0]) {
              slider.slider('values', 0, value);
            }
            $("#currentValue").html('$' + getRealValue(slider.slider('values', 0)));
            return false;
        },
        change: function(event, ui) { 
            getHomeListings();
        }
    });
    function findNearest(includeLeft, includeRight, value) {
        var nearest = null;
        var diff = null;
        for (var i = 0; i < values.length; i++) {
            if ((includeLeft && values[i] <= value) || (includeRight && values[i] >= value)) {
                var newDiff = Math.abs(value - values[i]);
                if (diff == null || newDiff < diff) {
                    nearest = values[i];
                    diff = newDiff;
                }
            }
        }
        return nearest;
    }
    function getRealValue(sliderValue) {
        for (var i = 0; i < values.length; i++) {
            if (values[i] >= sliderValue) {
                return trueValues[i];
            }
        }
        return 0;
    }
});