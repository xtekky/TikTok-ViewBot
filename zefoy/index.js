$(window).on("load", function() {
	ajaxHRS();
});

function ajaxHRS() {
	$("form").submit(function(event) {
		event.preventDefault();
		var hrefaction = $(this).attr("action");

		var formData = new FormData(this);
		$(".disableButton").prop("disabled", true);
		var ajaxSettings = {
			url: hrefaction,
			type: "POST",
			data: formData,
			contentType: false,
			cache: false,
			processData: false,
			timeout: 5e4
		};

		$.ajax(ajaxSettings).done(function(response) {
			$("#" + hrefaction).html(atob(decodeURIComponent(response.split("").reverse().join(""))));
			$("form").unbind();
			ajaxHRS();
			$(".disableButton").prop("disabled", false);

		}).fail(function(error) {
			$(".disableButton").prop("disabled", false);
			$(".wbutton,.spinner-border,.list-group").hide();
			$(".error").show();
		});
	});
};