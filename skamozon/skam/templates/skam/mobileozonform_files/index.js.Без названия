$(document).ready(() => {
	$("#myPhone").inputmask("+7 (999) 999-99-99");
	$('form[name="order-form"]').validate({
		errorElement: "div",
		errorClass: "_1sGhO _25DdM _3VXKX",
		highlight: function ( element, errorClass, validClass ) {
			$(element).parent().css({'border-color': '#fdb8cc', 'overflow': 'visible'});
		},
		unhighlight: function (element, errorClass, validClass) {
			$(element).parent().removeAttr('style');
		},
		submitHandler: function (form) {
			$('button[type="submit"]').attr('disabled', 'disabled');
			form.submit();
		}
	});
});