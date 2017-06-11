var last_index = 0;

function append_to_textarea(message, message_id) {
    if (message.type == "sys"){
        var text =  '<div class="well well-sm text-center system_message">' + "<b>" + message.author + '</b><br />'+ message.message +"</div>";
    }else{
        var text =  '<div class="well well-sm user_message">' +
            '<div style="float: right;" class=flag-rus>' +
                '<img style="display: block;" src="' + RUS_IMAGE_ICON + '" class = "translate_img" data-lang="ru" data-index='+ message_id + '>' +
            '</div>' +
            '<div class="author_mess">' +
                '<b>' + message.author + '</b>' +
            '</div>' +
            '<div style="float: right;" class="flag-eng">' +
                '<img style="display: block;" src="' + ENG_IMAGE_ICON + '" class = "translate_img" data-lang="en" data-index=' + message_id + '>' +
            '</div>' +
            '<div class="text_mess">'+ message.message + '</div>' +
        '</div>';
    }
    $("#chat-panel").append(text);
    if ($("#voice-check").prop("checked")){
        if (message.type != 'sys') {
            var text_to_play = message.author + ' сказал ' + message.plain_message;
            voice.addText(text_to_play);
        } else {
            var text_to_play = message.message;
            voice.addText(text_to_play);
        }
    };
};

function get_scrollHeight(element) {
    var pr = element.scrollTop();
    element.scrollTop(element.get(0).scrollHeight);
    var res = element.scrollTop();
    element.scrollTop(pr);
    return res;
}

function add_message(message, message_id) {
    last_index += 1;
    var t = false;
    if (get_scrollHeight($('#chat-panel')) == $('#chat-panel').scrollTop())
        t = true;
    append_to_textarea(message, message_id);
    if (t)
        $('#chat-panel').scrollTop($('#chat-panel').get(0).scrollHeight);
}

function get_messages(noti) {
    $.ajax({
        url: "/get_messages",
        data: {
            "chat": chat_index
        },
        dataType: "json",
        success: function(messages) {
            for (var i = last_index; i < messages.length; i++){
                add_message(messages[i], i);
                if (noti) notific(messages[i]);
            }
            last_index=messages.length;
        }
    });
}

function joinToChat(){
    $.ajax({
        type: "GET",
        url: "/add_chat",
        data: {
            chat: chat_index
        }
    });
}

jQuery(function($) {
    $("#message-input").keypress(function(e) {
        if(e.which == 13) {
            $("#send-btn").click();
        }
    });

    // translation
    $("#chat-panel").on("click", ".translate_img", function(){
        var lang = $(this).data('lang');
        var id = $(this).data('index');
        var text_obj = $(this).parents('.user_message').find('.text_mess');
        $.ajax({
            url: '/translate',
            data:{
                "chat": chat_index,
                "index": id
            },
            dataType: "json",
            success: function(data){
                text_obj.html(data[lang]);
            },
            error: function(data){
                if (lang == "ru")
                    alert('Извините, произошла ошибка при переводе!')
                if (lang == "en")
                    alert('Sorry, there was an error translating!')
            }
        });
    });

    if (!IS_USE_SOCKET) {
        joinToChat();
        get_messages(false);
        var timerId = setInterval(function (){
                    get_messages(true);
                    get_tree("tree");
                }, INTERVAL);
        $("#send-btn").click(function() {
            $.ajax({
                url: "/send_message",
                data: {
                    "chat": chat_index,
                    "message" : $("#message-input").val()
                }
            });
            $("#message-input").val('');
        });
    }
});