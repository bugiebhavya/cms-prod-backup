$(document).ready(function(){
	$(document).on('change', "[id$='area']",function(){
		var area_id = $(this).val()
        $.ajax({
            type: 'GET',
            url: '/filter/catalogs?object=0&type=area'.replace('0', area_id),
            data_type: 'json',
            success: function(response){
                if(response.code == 200){
                	$("[id$='subject']").empty()
                	$("[id$='topic']").empty()
                	$("[id$='subtopic']").empty()
                	subjects = "<option value=''>---------</option>"
                	response.data.forEach(function(vals){
                		subjects += "<option value='"+vals.id+"'>"+vals.name+"</option>"
                	})
                	$("[id$='subject']").append(subjects)
                }
            }
        })
    })

    $(document).on('change',"[id$='subject']",function(){
		var subject_id = $(this).val()
        $.ajax({
            type: 'GET',
            url: '/filter/catalogs?object=0&type=subject'.replace('0', subject_id),
            data_type: 'json',
            success: function(response){
                if(response.code == 200){
                	$("[id$='topic']").empty()
                	$("[id$='subtopic']").empty()
                	topic = "<option value=''>---------</option>"
                	response.data.forEach(function(vals){
                		topic += "<option value='"+vals.id+"'>"+vals.name+"</option>"
                	})
                	$("[id$='topic']").append(topic)
                }
            }
        })
    })

    $(document).on('change',"[id$='-topic']",function(){
		var topic_id = $(this).val()
        $.ajax({
            type: 'GET',
            url: '/filter/catalogs?object=0&type=topic'.replace('0', topic_id),
            data_type: 'json',
            success: function(response){
                if(response.code == 200){
                	$("[id$='subtopic']").empty()
                	subtopic = "<option value=''>---------</option>"
                	response.data.forEach(function(vals){
                		subtopic += "<option value='"+vals.id+"'>"+vals.name+"</option>"
                	})
                	$("[id$='subtopic']").append(subtopic)
                }
            }
        })
    })
    $(document).on('change',"#id_topic",function(){
		var topic_id = $(this).val()
        $.ajax({
            type: 'GET',
            url: '/filter/catalogs?object=0&type=topic'.replace('0', topic_id),
            data_type: 'json',
            success: function(response){
                if(response.code == 200){
                	$("#id_subtopic").empty()
                	subtopic = "<option value=''>---------</option>"
                	response.data.forEach(function(vals){
                		subtopic += "<option value='"+vals.id+"'>"+vals.name+"</option>"
                	})
                	$("#id_subtopic").append(subtopic)
                }
            }
        })
    })

})

