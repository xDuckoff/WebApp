jQuery(function($) {
    var TitleEditor = {
        block: $('.chat-title'),

        init: function() {
            this.viewer = this.block.find('.chat-title__viewer');
            this.title = this.block.find('.chat-title__title');
            this.editor = this.block.find('.chat-title__editor');
            this.input = this.block.find('.chat-title__input');
            this.save = this.block.find('.chat-title__save');
            this._prepareTitle();
            this._bindEvents();
        },

        _prepareTitle: function(){
            var title = this.title.children('p').html();
            if (title) {
                this.title.html(title);
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
                    me.changeTitle();
                }
            });
            me.save.on('click', function() {
                me.changeTitle();
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

        changeTitle: function() {
            var me = this,
                title = this.input.val();
            me.setLoading(true);
            $.ajax({
                url: "/set_chat_name",
                type: "POST",
                data: {
                    chat: CHAT_ID,
                    name: title
                },
                dataType: "json",
                success: function(response) {
                    if (response.success) {
                        me.setName(response.data);
                    }
                },
                complete: function() {
                    me.setLoading(false);
                }
            });
        },

        setName: function(names) {
            var me = this;
            this.title.html(names.original);
            this._prepareTitle();
            me.hideEditor();
            this.input.val(names.plain);
        },

        setLoading: function(isStart) {
            this.input.prop("disabled", isStart);
            this.save.prop("disabled", isStart);
            if (isStart) {
                this.block.addClass('chat-title_loading');
            } else {
                this.block.removeClass('chat-title_loading');
            }
        }
    };

    TitleEditor.init();
});
