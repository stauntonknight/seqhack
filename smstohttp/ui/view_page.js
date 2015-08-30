function delet(serviceName) {
	$.get('http://5bcafef9.ngrok.io/api/services/deleteservice', {
			'serviceName': serviceName
			}, function() {
				window.reload();
			});
}

$(document).ready(function() {
	$.get('http://5bcafef9.ngrok.io/api/services/listservices', function(serviceNames) {
		for (var i = 0 ; i < serviceNames.length; i++) {
			var $el = $($('#hidden-template-servicename').html());	
			$('#container').append($el);
			$el.find(".servicename").text(serviceNames[i]);
			var t = serviceNames[i];
			$el.find(".delete").click(function() {
				delet(t);
			});
		}
	});
});
