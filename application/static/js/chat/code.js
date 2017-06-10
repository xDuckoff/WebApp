function send_code() {
    $.ajax({
        url:"/send_code",
        type:"GET",
        data:{
            chat: chat_index,
            code: editor.getValue(),
            parent: parent_index,
            cname: $('#to_send').val()
        },
        dataType:'json',
        success: function(data){
            chosen_commit = data.commit;
        },
        error: function() {
            alert('Извините, произошла ошибка при загрузке кода!');
        }
    });
}
function get_code(codeId){
    codeId = codeId || startCommit;
    chosen_commit = codeId;
    $.ajax({
        url: "/get_code",
        type: "GET",
        data: {
            chat: chat_index,
            index: codeId
        },
        dataType: "json",
        success: function(data){
            parent_index = codeId;
            editor.getDoc().setValue(data.code);
        }
    });
}

jQuery(function($) {
    code_types = {
        "C": "text/x-csrc",
        "C#": "text/x-csharp",
        "C++": "text/x-c++src",
        "CSS": "text/css",
        "HTML": "text/html",
        "Java": "text/x-java",
        "JavaScript": "text/javascript",
        "Python": "text/x-python"
    };
    chat_code_type = code_types[chat_code_type];
    editor = CodeMirror.fromTextArea($('#code-editor').get(0), {
        mode: {
            name: chat_code_type,
            version: 2,
            singleLineStringErrors: false
        },
        lineNumbers: true,
        indentUnit: 4,
        matchBrackets: true,
        value: "print('Hello World!')"
    });
    get_code(0);

});
