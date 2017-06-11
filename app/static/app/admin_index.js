window.onload = function() {
	$(".center-right").children(":nth-of-type(n+2)").hide();
	$(".left").children(":first").children(":first").addClass("select");
}
var showhide = function(name) {
	$(".center-right").children().hide();
	$(".center-right").find(name).show();
	$(".left").children(":first").children().removeClass("select");
	$(".left").children(":first").find(name).addClass("select");
}