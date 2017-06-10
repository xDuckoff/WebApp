function notific(message){
    if (("Notification" in window) && (Notification.permission === "granted") && (message.type != "usr")) {
        var notification = new Notification(message.author, {body:message.plain_message});
        Notification.sound;
    }
    else if (Notification.permission !== 'denied') {
        Notification.requestPermission(function (permission) {
            if (permission === "granted") {
                var notification = new Notification(message.author, {body:message.plain_message});
                Notification.sound;
            }
        });

    }
}
