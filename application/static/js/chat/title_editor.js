jQuery(function($) {
    var TitleEditor = {
        block: $('.chat-title'),

        init: function() {
            this.viewer = this.block.find('.chat-title__viewer');
            this.editButton = this.block.find('.chat-title__edit');
            this.editor = this.block.find('.chat-title__editor');
            this.input = this.block.find('.chat-title__input');
            this.save = this.block.find('.chat-title__save');
            this._initListeners();
        },

        _initListeners: function() {
            var me = this;
            me.editButton.on('click', function() {
                me.showEditor();
            });
            me.input.on('blur', function() {
                me.hideEditor();
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
            // TODO отправить запрос на сервер для сохранения заголовка
        }
    };

    TitleEditor.init();
});
