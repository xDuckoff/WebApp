jQuery(function ($) {
    $('#compare').on('shown.bs.modal', function () {
        $.ajax({
            url:"/get_code",
            type:"GET",
            data:{
                chat: chat_index,
                index: startCommit
            },
            dataType: "json",
            success: function(data){
                var target = $("#comp");
                target.empty();
                dv = CodeMirror.MergeView(target[0], {
                    value: editor.getValue(),
                    origLeft: data.code,
                    mode: {
                        name: chat_code_type,
                        version: 2,
                        singleLineStringErrors: false
                    },
                    lineNumbers: true,
                    highlightDifferences: true,
                    readOnly: true,
                    revertButtons: false
                });
            }
        });
    });
    $('#compare-btn').click(function () {
        $('#compare').modal("show");
    });
    $('#close-btn').click(function () {
        $('#compare').modal("hide");
    });
});