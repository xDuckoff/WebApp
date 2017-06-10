jQuery(function($){
    window.voice = {
        stack: [],
        currentIndex: -1,
        isBusy:false,

        play: function(){
            this.isBusy = true;
            this.currentIndex++;
            var url = 'https://tts.voicetech.yandex.net/generate?' +
                'key=2308bf65-4316-45e9-bcec-0f9d86a7ab63' +
                '&text=' + encodeURI(this.stack[this.currentIndex]) +
                '&fornat=wav' +
                '&lang=ru-RU' +
                '&speaker=jane';

            this.audio.src = url;
            this.audio.load();
        },
        init: function() {
            this.audio = $('#audio')[0];
            this.audio.onloadeddata = function(){
                voice.audio.play();
            };
            this.audio.onended = function(){
                voice.checkEnd();
            };
        },
        checkEnd: function(){
            this.isBusy = false;
            this.checkPlay();
        },
        checkPlay: function (){
            if (!this.isBusy &&  this.stack.length != (this.currentIndex + 1) ){
                this.play();
            }
        },
        addText: function(text){
            this.stack.push(text);
            this.checkPlay();

        }
    };
    voice.init();
});