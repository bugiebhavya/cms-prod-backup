$(document).ready(function(){
	$(".fav-button").click(function(){
		/*
            Function alters value of form button between positive and negative notations.
            object_id for Integrity, form and input fields are selected with respect to object_id
        */
        var positive_notation = $("input[name=positive_notation]").val();
	    var negative_notation = $("input[name=negative_notation]").val();
        var object_id = $(this).attr("object");
        var form = ".fav-form"+ object_id ;
        var button = '#fav-button'+object_id;
        var button_value = $(this).val();
        var data =  new FormData($(form).get(0));
        var fav_count_div = ".fav_count_div" + object_id;
        var fav_count_field = "#fav_count"+object_id;
        var fav_count_val = parseInt($("#fav_count"+object_id).val());
       	if(button_value == positive_notation) {
       		data.append('fav_value',positive_notation);
       	}
       	else{
       		data.append('fav_value',negative_notation);
     	}
		$.ajax({
            url: "/en/medias/fav/",
            type: "POST",
            data: data,
            processData: false,
            contentType: false,
            success: function(response) {
            	if (response['success'] == 0) {
	                  alert(response['error'])   
	                }
            	else {
	            	$(fav_count_div).empty();
	            	$(button).closest('.fav-btn').removeClass($(button).val())
	            	if(button_value == positive_notation) {
	            		fav_count_val = fav_count_val+1;
	                    $(button).val(negative_notation);
	                  	
	                  }
	                  else{
	                  	fav_count_val = fav_count_val-1;
                        $(button).val(positive_notation);
	                  }
	                $(button).closest('.fav-btn').addClass($(button).val())
	                // Token maintained for multiple submissions of form(s).
	                $("input[name=csrfmiddlewaretoken]").val(response['csrf']);
	                $(fav_count_field).val(fav_count_val);
	                $(fav_count_div).append(fav_count_val);		            	
				}
            },
            error: function(response) {
            	alert("error")
            }
        }); 
	});
});