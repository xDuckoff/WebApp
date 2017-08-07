jQuery(function ($) {
    window.CodeCompare = {
        element: $('#code-compare'),
        field: null,
        startCode: null,

        init: function() {
            this.field = this.element.find('.code-compare__field');
            this._loadStartCode();
            this._bindEvents();
        },

        _loadStartCode: function() {
            $.ajax({
                url: "/get_code",
                data: {
                    chat: CHAT_ID,
                    index: CODE_START_COMMIT
                },
                dataType: "json",
                success: function(data){
                    CodeCompare.startCode = data.code;
                }
            });
        },

        _setCodeMirrorToField: function() {
            CodeMirror.MergeView(this.field[0], {
                value: CodeEditor.getCode(),
                origLeft: this.startCode,
                mode: {
                    name: CODE_TYPE,
                    version: 2,
                    singleLineStringErrors: false
                },
                lineNumbers: true,
                highlightDifferences: true,
                readOnly: true,
                revertButtons: false
            });
        },

        _bindEvents: function() {
            this.element.on('shown.bs.modal', function() {
                CodeCompare._setCodeMirrorToField();
            });
            this.element.on('hidden.bs.modal', function() {
                CodeCompare.field.empty();
            });
        }
    };
    CodeCompare.init();
});