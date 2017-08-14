jQuery(function($) {
    window.MessagesArea = {
        SYSTEM_TEMPLATE: "<div class=\"well well-sm system-message\">" +
            "<div class=\"system-message__author\">{{author}}</div>" +
            "<div class=\"system-message__content\">{{content}}</div>" +
        "</div>",
        USER_TEMPLATE: "<div class=\"well well-sm user-message\">" +
            "<div class=\"user-message__author\">{{author}}</div>" +
            "<div class=\"user-message__content\">{{content}}</div>" +
        "</div>",
        SYSTEM_TYPE: 'sys',
        element: $('.chat-panel'),
        area: null,
        content: null,
        lastMessageId: null,
        _watchTimer: null,

        init: function() {
            this.content = this.element.find('.chat-panel__content');
            this.area = this.element.find('.chat-panel__messages');
            this.getExistMessages();
            this.watch();
        },

        watch: function() {
            if (IS_USE_SOCKET) {
                ChatSocket.on('message', function(message) {
                    MessagesArea.addMessage(message, true);
                });
            } else {
                this._watchTimer = setInterval(function() {
                    MessagesArea.checkNewMessages(true);
                }, INTERVAL);
            }
        },

        getExistMessages: function() {
            $.ajax({
                url: "/get_messages",
                type: "GET",
                data: {
                    chat: CHAT_ID
                },
                dataType: "json",
                success: function(messages) {
                    MessagesArea.renderMessages(messages);
                }
            });
        },

        renderMessages: function(messages, isNotify) {
            isNotify = isNotify || false;
            for (var i = 0; i < messages.length; i++) {
                this.addMessage(messages[i], isNotify);
            }
        },

        addMessage: function(message, isNotify) {
            isNotify = isNotify || false;
            if (message.type === this.SYSTEM_TYPE){
                this.renderSystemMessage(message);
            } else {
                this.renderUserMessage(message);
            }
            this.lastMessageId = message.id;
            this.scrollToEnd();
            if (isNotify) {
                this.doNotification(message);
                this.soundMessage(message);
            }
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
            this.content.scrollTop(areaHeight);
        },

        checkNewMessages: function() {
            $.ajax({
                url: "/get_messages",
                type: "GET",
                data: {
                    chat: CHAT_ID,
                    last_message_id: this.lastMessageId
                },
                dataType: "json",
                success: function(messages) {
                    MessagesArea.renderMessages(messages, true);
                }
            });
        },

        doNotification: function(message) {
            if (message.type !== 'mine') {
                Push.create(message.author, {
                    body: message.plain_message,
                    icon: MAIN_ICON_URL,
                    timeout: 4000
                });
            }
        },

        soundMessage: function(message) {
            var soundText;
            if (message.type !== this.SYSTEM_TYPE) {
                soundText = message.author + ' написал ' + message.plain_message;
            } else {
                soundText = message.plain_message;
            }
            VoiceKit.addQueueItem(soundText);

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
                if ( !e.shiftKey && e.which === 13 ) {
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
                    type: "POST",
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
});