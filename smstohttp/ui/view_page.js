function delet(serviceName) {
	$.get('/deleteservice', serviceName, window.reload);
}

$(document).ready(function() {
	$.get('/listservice', function(serviceNames) {
		for (var i = 0 ; i < serviceNames.length; i++) {
			var $el = $($('#hidden-template-servicename').html());	
			$el.find(".servicename").text(serviceNames[i]);
			$el.find(".delete").click(function() {
				delet(serviceNames[i]);
			});
			$('#container').append($el);
		}
	});
});
