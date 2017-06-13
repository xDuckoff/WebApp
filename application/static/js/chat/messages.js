function joinToChat(){
    $.ajax({
        type: "GET",
        url: "/join_chat",
        data: {
            chat: chat_index
        }
    });
}

jQuery(function($) {
    var CHAT_ID = chat_index;
    window.MessagesArea = {
        SYSTEM_TEMPLATE: "<div class=\"well well-sm system-message\">" +
            "<div class=\"system-message__author\">{{author}}</div>" +
            "<div class=\"system-message__content\">{{content}}</div>" +
        "</div>",
        USER_TEMPLATE: "<div class=\"well well-sm user-message\">" +
            "<div class=\"user-message__author\">{{author}}</div>" +
            "<div class=\"user-message__content\">{{content}}</div>" +
        "</div>",
        element: $('.chat-panel'),
        area: null,
        lastMessageId: null,
        _watchTimer: null,

        init: function() {
            this.area = this.element.find('.chat-panel__messages');
            this.getExistMessages();
            this.watch();
        },

        watch: function() {
            if (!IS_USE_SOCKET) {
                this._watchTimer = setInterval(function() {
                    MessagesArea.checkNewMessages(true);
                    //get_tree("tree");
                }, INTERVAL);
            }
        },

        getExistMessages: function() {
            $.ajax({
                url: "/get_messages",
                data: {
                    chat: CHAT_ID
                },
                dataType: "json",
                success: function(messages) {
                    MessagesArea.renderMessages(messages);
                }
            });
        },

        renderMessages: function(messages) {
            for (var i = 0; i < messages.length; i++) {
                this.addMessage(messages[i]);
                //if (noti)
                //    notific(messages[i]);
            }
        },

        addMessage: function(message) {
            if (message.type === "sys"){
                this.renderSystemMessage(message);
            } else {
                this.renderUserMessage(message);
            }
            this.lastMessageId = message.id;
            this.scrollToEnd();
            // TODO
            //if ($("#voice-check").prop("checked")){
            //    if (message.type != 'sys') {
            //        var text_to_play = message.author + ' сказал ' + message.plain_message;
            //        voice.addText(text_to_play);
            //    } else {
            //        var text_to_play = message.message;
            //        voice.addText(text_to_play);
            //    }
            //};
        },

        renderSystemMessage: function(message) {
            var messageEl = this.SYSTEM_TEMPLATE.replace('{{author}}', message.author)
                    .replace('{{content}}', message.message);
            messageEl = $(messageEl);
            messageEl.data('id', message.id);
            this.area.append(messageEl);
        },

        renderUserMessage: function(message) {
            var messageEl = this.USER_TEMPLATE.replace('{{author}}', message.author)
                    .replace('{{content}}', message.message);
            messageEl = $(messageEl);
            messageEl.data('id', message.id);
            this.area.append(messageEl);
        },

        scrollToEnd: function() {
            var areaHeight = this.area.outerHeight(true);
            this.element.scrollTop(areaHeight);
        },

        checkNewMessages: function() {
            $.ajax({
                url: "/get_new_messages",
                data: {
                    chat_id: CHAT_ID,
                    last_message_id: this.lastMessageId
                },
                dataType: "json",
                success: function(messages) {
                    MessagesArea.renderMessages(messages);
                }
            });
        }
    };

    window.MessageSender = {
        element: $('.message-sender'),
        content: null,
        toSend: null,

        init: function() {
            this.content = this.element.find('.message-sender__content');
            this.toSend = this.element.find('.message-sender__to-send');
            this._bindEvents();
        },

        _bindEvents: function() {
            this.content.on('keypress', function(e) {
                if(e.which == 13) {
                    MessageSender.send();
                }
            });
            this.toSend.on('click', function() {
                MessageSender.send();
            });
        },

        send: function() {
            if ( this.isValid() ) {
                $.ajax({
                    url: "/send_message",
                    data: {
                        "chat": CHAT_ID,
                        "message": this.content.val()
                    },
                    success: function() {
                        MessageSender.clear();
                    }
                });
            }
        },

        clear: function() {
            this.content.val("");
        },

        isValid: function() {
            return !!this.content.val();
        }
    };

    MessagesArea.init();
    MessageSender.init();

    if (!IS_USE_SOCKET) {
        joinToChat();
    }
});