jQuery(function ($) {
    joinToChat();
    get_messages(false);
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('join', chat_index);
    });
    socket.on('disconnect', function() {
        socket.emit('leave', chat_index);
    });

    socket.on('message', function(data) {
        add_message(data, last_index);
        notific(data);
    });

    socket.on('commit', function() {
        get_tree("tree");
    });
    $("#send-btn").click(function() {
        socket.emit('message', {
            'message': $("#message-input").val(),
            'room': chat_index,
            'type':'usr'
        });
        $("#message-input").val('');
    });
});
