$(document).ready(function() {
	$("#searchbutton").click(function() {
		var text = $("#locationTextField").val();
		var parm = "\\?exclude\\=currently,flags,minutely,hourly";
		//var request = $.get("/searchLocation/" + $("#locationTextField").val());
		window.location=  "/searchLocation/" + $("#locationTextField").val();

	})
})