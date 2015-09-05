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
		api['parameters'] = [];
		$(this).find(".paramval").each(function() {
		    api['parameters'].push($(this).val());
		});
		apis.push(api);
	});
	var service = {};
	service['headers'] = {};
	$(this).find(".headerentry").each(function() {
				headerKey = $(this).find('.headertxt').val()
		headerVal = $(this).find('.headerval').val()
		service['headers'][headerKey] = headerVal;
    });
	
	service['provider'] = provider;
	service['endpoint'] = $('#apibaseurl').val();
	service['apis'] = apis;
	$.post('http://localhost:50467/api/Services/AddApi', service);
	e.preventDefault();
});

