jQuery(function() {
    window.ChatSocket = io.connect(location.origin);
    ChatSocket.on('connect', function() {
        ChatSocket.emit('join', CHAT_ID);
    });
    ChatSocket.on('disconnect', function() {
        ChatSocket.emit('leave', CHAT_ID);
    });
});
