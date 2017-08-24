jQuery(function($) {
    var NameEditor = {
        block: $('.chat-name'),

        init: function() {
            this.viewer = this.block.find('.chat-name__viewer');
            this.title = this.block.find('.chat-name__title');
            this.editor = this.block.find('.chat-name__editor');
            this.input = this.block.find('.chat-name__input');
            this.save = this.block.find('.chat-name__save');
            this._prepareName();
            this._bindEvents();
        },

        _prepareName: function(){
            var name = this.title.children('p').html();
            if (name) {
                this.title.html(name);
            }
        },

        _bindEvents: function() {
            var me = this;
            me.viewer.on('click', function() {
                me.showEditor();
            });
            $('body').on('click', function(e) {
                if (!me.block.is( e.target ) && me.block.has( e.target ).length === 0) {
                    me.hideEditor();
                }
            });
            this.input.on('keypress', function(e) {
                if ( e.which === 13 ) {
                    me.changeName();
                }
            });
            me.save.on('click', function() {
                me.changeName();
            });
        },

        showEditor: function() {
            this.viewer.hide();
            this.editor.css('display', 'table');
            this.input.focus();
        },

        hideEditor: function() {
            this.viewer.show();
            this.editor.hide();
        },

        changeName: function() {
            var me = this,
                name = this.input.val();
            if (name) {
                me.setLoading(true);
                $.ajax({
                    url: "/set_chat_name",
                    type: "POST",
                    data: {
                        chat: CHAT_ID,
                        name: name
                    },
                    dataType: "json",
                    success: function (response) {
                        if (response.success) {
                            me.setName(response.data);
                        } else {
                            me.hideEditor();
                        }
                    },
                    complete: function () {
                        me.setLoading(false);
                    }
                });
            } else {
                me.hideEditor();
            }
        },

        setName: function(names) {
            var me = this;
            this.title.html(names.original);
            this._prepareName();
            me.hideEditor();
            this.input.val(names.plain);
        },

        setLoading: function(isStart) {
            this.input.prop("disabled", isStart);
            this.save.prop("disabled", isStart);
            if (isStart) {
                this.block.addClass('chat-name_loading');
            } else {
                this.block.removeClass('chat-name_loading');
            }
        }
    };

    NameEditor.init();
});
