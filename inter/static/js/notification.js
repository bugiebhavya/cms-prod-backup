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