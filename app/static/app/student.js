window.onload = function() {
	$(".center").children(":nth-of-type(n+2)").hide();
	$(".left").children(":first").children(":first").addClass("select");
	getMark();
}
var showhide = function(name) {
	$(".center").children().hide();
	$(".center").find(name).show();
	$(".left").children(":first").children().removeClass("select");
	$(".left").children(":first").find(name).addClass("select");
}
var setMark = function() {
	var title = document.getElementById("markTitle").value;
	var content = document.getElementById("markContent").value;
	if(title == "" || content == "") {
		alert("记录不能为空");
		return 1;
	}
	var count = localStorage.getItem("count");
	if(count == null) {
		count = 0;
	} else {
		count = parseInt(count) + 1;
	}
	localStorage.setItem("count", count);
	localStorage.setItem("title"+count, title);
	localStorage.setItem("content"+count, content);
	history.go(0);
}
var getMark = function() {
	var count = localStorage.getItem("count");
	if(count == null) {
		return 0;
	}
	var title;
	var content;
	var accordion = document.getElementsByClassName("accordion")[1]; 
	for(i=0; i<=count; i++) {
		title = localStorage.getItem("title"+i);
		content = localStorage.getItem("content"+i);
		
		var titleElement = document.createElement("h5");
		titleElement.innerHTML = title;
		var contentElement = document.createElement("div");
		contentElement.innerHTML = content;
		
		accordion.appendChild(titleElement);
		accordion.appendChild(contentElement);
	}
	$(function() {
		$(".accordion").accordion({
			heightStyle: "content",
			collapsible: true
		});
	});
}
var removeMark = function() {
	var removeTitle = document.getElementById("removeTitle").value;
	var count = localStorage.getItem("count");
	if(count == null) {
		return 0;
	}
	var k = 0;
	for(i=0; i<=count; i++) {
		if(removeTitle == localStorage.getItem("title"+i)) {
			for(j=i; j<count; j++) {
				localStorage.setItem("title"+j, localStorage.getItem("title"+(j+1)));
				localStorage.setItem("content"+j, localStorage.getItem("content"+(j+1)));
			}
			k = parseInt(k) + 1;
		}
	}
	for(i=0; i<k; i++) {
		localStorage.removeItem("title"+count);
		localStorage.removeItem("content"+count);
		count = parseInt(count) - 1;
	}
	localStorage.setItem("count", count);
}
