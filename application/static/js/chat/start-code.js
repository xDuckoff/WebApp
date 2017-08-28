jQuery(function($) {

    window.StartCodeEditor = {
        field: null,

        init: function() {
            this.setCodeMirrorToField();
        },

        setCodeMirrorToField: function() {
            var field = $('.start-code-sender__code-editor').get(0);
            this.field = CodeMirror.fromTextArea(field, {
                mode: {
                    name: "text/x-python",
                    version: 2,
                    singleLineStringErrors: false
                },
                lineNumbers: true,
                indentUnit: 4,
                matchBrackets: true,
                value: "print 'Hello, world!'"
            });
        },

        getCode: function() {
            return this.field.getValue();
        }
    };

    window.StartCodeSender = {
        element: $('#start-code-sender'),
        message: null,
        toSend: null,
        init: function() {
            this.code_type = this.element.find('.start-code-sender__code-type') ;
            this.code = this.element.find('.start-code-sender__code');
            this.toSend = this.element.find('start-code-sender__to-send')
            this._bindEvents();
        },

        _bindEvents: function() {
            this.toSend.on('click', function() {
                StartCodeSender.send();
            });
        },

        send: function() {
            $.ajax({
                url: "/init_chat",
                type: 'POST',
                data: {
                    chat: CHAT_ID,
                    code: this.StartCodeEditor.getCode(),
                    code_type: this.code_type.getValue()
                },
                dataType: "json"
            });
            this.element.modal('hide');
        },
    };

    StartCodeEditor.init();
    StartCodeSender.init();
});
