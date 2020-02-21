document.addEventListener('DOMContentLoaded', function() {
    if (!Notification) {
        alert('Desktop notifications not available in your browser.');
        return;
    }

    if (Notification.permission !== 'granted')
        Notification.requestPermission();
});


function notifyMe(title, url, image_url, body) {
    if (Notification.permission !== 'granted')
        Notification.requestPermission();
    else {
        var notification = new Notification(title, {
            icon: image_url,
            body: body,
        });
        notification.onclick = function() {
            window.open(url);
        };
    }
}

$(document).ready(function(){
    var template = '<a href="{0}" class="notification-block" data-id="{3}">\
                    <div class="icon"><img class="profile-pic" src="{1}" alt="media"></div>\
                    <div class="notification-text">{2}</div>\
              </a>'
    $.ajax({
        type: 'get',
        url: '/api/notifications',
        success: function(response){
            console.log(response)
            response.data.forEach(function(notification){
                var title = "Un nuevo contenido está disponible <b>"+notification.content.title+"<b>"
                $(".notification-list").prepend(template.f(notification.content.link_url, notification.content.thumbnail, title, notification.id))
            })
            $('.notification-count').text(response.data.length)
        }
    })
})

$(document).on('click', '.notification-block', function(e){
    e.preventDefault()
    var redirect_url = $(this).attr('href')
    $.ajax({
        type: 'get',
        url: '/api/notifications/'+$(this).attr('data-id')+'/remove',
        success: function(response){
            if(response.code == 200){
                location.href = redirect_url
            }
        }
    })
})