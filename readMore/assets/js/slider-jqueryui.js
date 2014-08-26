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
    var trueValues = [5, 10, 50, 100, 500, 1000, 2500, 5000, 7500, 10000, 20000, 30000, 40000, 50000, 60000, 70000];
    var values =     [0,  6,  12,   18,   24,    30,    36,    42,   48,   54,     60,     66,   74,    82,    90,   100];
    var slider = $("#slider").slider({
        orientation: 'horizontal',
        range: false,
        min: 5,
        max: 100,
        values: [0],
        slide: function(event, ui) {
            var includeLeft = event.keyCode != $.ui.keyCode.RIGHT;
            var includeRight = event.keyCode != $.ui.keyCode.LEFT;
            var value = findNearest(includeLeft, includeRight, ui.value);
            if (ui.value == ui.values[0]) {
              slider.slider('values', 0, value);
            }
            $("#currentValue").html(getRealValue(slider.slider('values', 0)));
            return false;
        },
        change: function(event, ui) { 
            //getHomeListings();
            initialize();
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

$(function() {
    var trueValues = [5, 10, 50, 100, 150, 200, 250, 300, 400, 500];
    var values =     [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
    var slider = $("#slider2").slider({
        orientation: 'horizontal',
        range: false,
        min: 5,
        max: 100,
        values: [0],
        slide: function(event, ui) {
            var includeLeft = event.keyCode != $.ui.keyCode.RIGHT;
            var includeRight = event.keyCode != $.ui.keyCode.LEFT;
            var value = findNearest(includeLeft, includeRight, ui.value);
            if (ui.value == ui.values[0]) {
              slider.slider('values', 0, value);
            }
            $("#currentValue2").html(getRealValue(slider.slider('values', 0)));
            return false;
        },
        change: function(event, ui) { 
            initialize();
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

function get_curr() {
    return $('#currentValue').html(this.value);
}

function get_curr2() {
    return $('#currentValue2').html(this.value);
}

