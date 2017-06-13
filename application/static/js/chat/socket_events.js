function joinToChat(){
    $.ajax({
        type: "GET",
        url: "/join_chat",
        data: {
            chat: chat_index
        }
    });
}

jQuery(function() {
    var CHAT_ID = chat_index;
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('join', CHAT_ID);
    });

    socket.on('disconnect', function() {
        socket.emit('leave', CHAT_ID);
    });

    socket.on('message', function(message) {
        MessagesArea.addMessage(message);
        // notific(data);
    });

    socket.on('commit', function() {
        // TODO
        // get_tree("tree");
    });

    joinToChat();
});
