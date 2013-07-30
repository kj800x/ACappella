function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//** IMPLEMENTATION SPECIFIC CODE **//

function channeldelete(chanid){
	$.ajax(
		{
	  		type: "POST",
	  		url: "./channeldelete/",
	  		data: { "id": chanid },
	  		success: function(data) {
	  			 $("#chan_"+chanid).fadeOut(500, function() { $("#chan_"+chanid).remove(); });
	  		},
	  		error: function(data) {
	  			$("#errorbox").text(data.responseText);
	  			$("#errorbox").fadeOut(10000);
	  		}
		}
	);
}

function channelmove(chanid, whichdirection){
	$.ajax(
		{
	  		type: "POST",
	  		url: "./channelmove/",
	  		data: { "id": chanid, "whichdirection": whichdirection },
	  		success: function(data) {
	  			a = data;
	  			swaparrays = data.split(",");
	  			$("#chan_"+swaparrays[0]).before($("#chan_"+swaparrays[1]));
	  		},
	  		error: function(data) {
	  			$("#errorbox").text(data.responseText);
	  			$("#errorbox").fadeOut(10000);
	  		}
		}
	);
}

function channelrename(chanid, newname){
	$.ajax(
		{
	  		type: "POST",
	  		url: "./channelrename/",
	  		data: { "id": chanid, "newname": newname },
	  		success: function(data) {
	  			$("#chan_"+chanid+"_title").text(newname);
	  		},
	  		error: function(data) {
	  			$("#errorbox").text(data.responseText);
	  			$("#errorbox").fadeOut(10000);
	  		}
		}
	);
}

function edithit(id, label, seconds_Mark){
	$.ajax(
		{
	  		type: "POST",
	  		url: "./edithit/",
	  		data: { "id": id, "seconds_Mark": seconds_Mark, "label": label },
	  		success: function(data) {
	  		  $("#hit_"+id+"_label").text(label);
	  		  $("#hit_"+id+"_seconds").text(seconds_Mark);
	  		},
	  		error: function(data) {
	  			$("#errorbox").text(data.responseText);
	  			$("#errorbox").fadeOut(10000);
	  		}
		}
	);
}

function deletehit(id){
	$.ajax(
		{
	  		type: "POST",
	  		url: "./deletehit/",
	  		data: { "id": id },
	  		success: function(data) {
	  			 $("#hit_"+id).fadeOut(500, function() { $("#hit_"+id).remove(); });
	  		},
	  		error: function(data) {
	  			$("#errorbox").text(data.responseText);
	  			$("#errorbox").fadeOut(10000);
	  		}
		}
	);
}


function deletepdf(id){
	$.ajax(
		{
	  		type: "POST",
	  		url: "./deletepdf/",
	  		data: { "id": id },
	  		success: function(data) {
	  			 $("#pdfblock").text("UPLOAD A PDF");
	  			 $("#pdfblock").attr('href', './pdf/')
	  			 $('#pdfblock').attr('onclick','').unbind('click');
	  		},
	  		error: function(data) {
	  			$("#errorbox").text(data.responseText);
	  			$("#errorbox").fadeOut(10000);
	  		}
		}
	);
}