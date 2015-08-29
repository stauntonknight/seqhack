$('#addAPI').click(function() {
	var html = $('#hidden-template').html()
	$('#apiinfo').append(html)
});

$('#container').on('click', '.addParam', function(e) {
	$(e.target.nextElementSibling).append($('#hidden-template-param').html());
});

$('#container').submit(function(e) {
	var provider = $('#provider').val();
	var apis = [];
	$('.apidetail').each(function() {
		var api = {};
		api['name'] = $(this).find(".apiname").val()
		api['params'] = [];
		$(this).find(".paramval").each(function() {
			api['params'].push($(this).val());
		});
		apis.push(api);
	});
	e.preventDefault();
});

