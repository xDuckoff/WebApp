jQuery(function($) {
    window.CodeEditor = {
        field: null,

        init: function() {
            this.setCodeMirrorToField();
        },

        setCodeMirrorToField: function() {
            var field = $('.code-editor').get(0);
            this.field = CodeMirror.fromTextArea(field, {
                mode: {
                    name: CODE_TYPE,
                    version: 2,
                    singleLineStringErrors: false
                },
                lineNumbers: true,
                indentUnit: 4,
                matchBrackets: true,
                value: "print('Hello World!')"
            });
        },

        getCode: function() {
            return this.field.getValue();
        },

        setCode: function(codeId) {
            $.ajax({
                url: "/get_code",
                type: 'GET',
                data: {
                    chat: CHAT_ID,
                    index: codeId
                },
                dataType: "json",
                success: function(data){
                    CodeEditor.currentCommit = codeId;
                    CodeEditor.field
                        .setValue(data.code);
                }
            });
        },

        sendCode: function(message) {
            $.ajax({
                url:"/send_code",
                type:"POST",
                data: {
                    chat: CHAT_ID,
                    code: CodeEditor.getCode(),
                    parent: this.currentCommit,
                    message: message
                },
                dataType:'json',
                success: function(data){
                    CodeEditor.currentCommit = data.commit;
                },
                error: function() {
                    alert('Извините, произошла ошибка при сохранении кода!');
                }
            });
        }
    };

    window.CodeTree = {
        canvas: $('.code-tree'),
        config: {
            container: '.code-tree',
            levelSeparation: 70,
            siblingSeparation: 70,
            rootOrientation: "WEST",
            connectors: {
                style: {
                    stroke: 'white'
                }
            }
        },

        init: function() {
            this.update();
            this.canvas.on("click", ".commit_node", function(){
                var codeId = $(this).data('id');
                CodeTree.highlightNode(codeId);
                CodeEditor.setCode(codeId);
            });
            this.watch();
        },

        watch: function() {
            if (IS_USE_SOCKET) {
                ChatSocket.on('commit', function() {
                    CodeTree.update();
                });
            } else {
                this._watchTimer = setInterval(function() {
                    CodeTree.update();
                }, INTERVAL);
            }
        },

        update: function() {
            $.ajax({
                url: "/tree",
                type: 'GET',
                data: {
                    chat: CHAT_ID
                },
                dataType: "json",
                success: function( data ) {
                    CodeTree.render(data);
                }
            });
        },

        render: function(data) {
            var simple_chart_config = {
                    chart: $.extend({}, this.config),
                    nodeStructure: data
                };
            new Treant(simple_chart_config, function(){
                CodeTree.highlightNode(CodeEditor.currentCommit);
            }, $);
        },

        highlightNode: function(codeId) {
            var nodes = this.canvas.find('.commit_node');
            nodes.removeClass('chosen')
                    .filter('[data-id=' + codeId + ']')
                    .addClass('chosen');
        }
    };

    window.CodeSender = {
        element: $('#code-sender'),
        message: null,
        toSend: null,
        init: function() {
            this.message = this.element.find('.code-sender__message') ;
            this.toSend = this.element.find('.code-sender__to-send');
            this._bindEvents();
        },

        _bindEvents: function() {
            this.element.on('shown.bs.modal', function () {
                CodeSender.message.focus();
            });
            this.element.on('hidden.bs.modal', function () {
                CodeSender.clear();
            });
            this.toSend.on('click', function() {
                CodeSender.send();
            });
            this.message.on('keypress', function(e) {
                if ( e.which === 13 ) {
                    CodeSender.send();
                }
            });
        },

        clear: function() {
            this.message.val('')
                .parent('.form-group')
                .removeClass('has-error')
        },

        send: function() {
            if (this.isValid()) {
                CodeEditor.sendCode(this.message.val());
                this.element.modal('hide');
            }
        },

        isValid: function() {
            if ( !this.message.val() ) {
                this.message
                    .parent('.form-group')
                    .addClass('has-error');
                return false;
            }
            return true;
        }
    };

    CodeEditor.init();
    CodeTree.init();
    CodeSender.init();
});
