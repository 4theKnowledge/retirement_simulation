$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				name : $('#nameInput').val(),
				email : $('#emailInput').val()
			},
			type : 'POST',
			url : '/simulate_input_data'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

    });
    
    $('button').on('submit', function(event() {
        $.ajax({
            data : {
                simulate : 'True'
            },
        type : 'POST',
        url : '/simulate'
        })
    });

    event.preventDefault();

});