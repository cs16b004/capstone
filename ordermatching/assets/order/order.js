$("#id_order_type").change(function(){
	// alert("k")
	if ($(this).val() == "MR") {

		$("#id_all_or_none").prop("checked",true)
		$("#id_all_or_none").prop("disabled",true)
		$('#id_Minimum_fill').prop('disabled', true);
		$('#id_Disclosed_Quantity').prop('disabled', true);
		$('#id_order_price').prop('disabled', true);
	}
	else {
		$("#id_all_or_none").prop("disabled",false)
		$("#id_all_or_none").prop("checked",false)
		$('#id_Minimum_fill').prop('disabled', false);
		$('#id_Disclosed_Quantity').prop('disabled', false);
		$('#id_order_price').prop('disabled', false);
	}
})

$("#id_all_or_none").change(function(){
	// alert("ok")
	if ($(this).is(':checked')){
		$('#id_Minimum_fill').prop('disabled', true);
		$('#id_Disclosed_Quantity').prop('disabled', true);
	}
	else {
		$('#id_Minimum_fill').prop('disabled', false);
		$('#id_Disclosed_Quantity').prop('disabled', false);
	}
})

$( function () {
	$("#myModal").draggable({
      handle: ".modal-header"
	}); 
});