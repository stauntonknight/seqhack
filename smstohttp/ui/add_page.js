$('#addAPI').click(function() {
	var html = $('#hidden-template').html()
	$('#apiinfo').append(html)
});

$('#container').on('click', '.addParam', function(e) {
	$(e.target.nextElementSibling).append($('#hidden-template-param').html());
});

$('#container').on('click', '.addHeader', function(e) {
	$(e.target.nextElementSibling).append($('#hidden-template-header').html());
});


$('#container').submit(function(e) {
	var provider = $('#provider').val();
	var apis = [];
	$('.apidetail').each(function() {
		var api = {};
		api['name'] = $(this).find(".apiname").val()
		api['resourceUrl'] = $(this).find(".apiurl").val()
		api['params'] = [];
		$(this).find(".paramval").each(function() {
			api['params'].push($(this).val());
		});
		apis.push(api);
	});
	apis['headers'] = [];
	$(this).find(".headerentry").each(function() {
		var header = {};
		headerKey = $(this).find('.headertxt').val()
		headerVal = $(this).find('.headerval').val()
		header[headerKey] = headerVal;
		apis['headers'].push(header);
    });
	var service = {};
	service['provider'] = provider;
	service['endpoint'] = $('#apibaseurl').val();
	$.post('/addapi', service);
	e.preventDefault();
});

