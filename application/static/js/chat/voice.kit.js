jQuery(function($){
    window.VoiceKit = {
        element: $('.voice'),
        audio: null,
        switcher: null,
        queue: [],
        currentIndex: -1,
        isBusy: false,

        init: function() {
            this.audio = this.element.find('.voice__audio')[0];
            this.switcher = this.element.find('.voice__switcher');
            var storedVoiceSwitchState = localStorage.getItem('chat-voice-switcher') === 'true';
            this.switcher.prop('checked', storedVoiceSwitchState);
            this._bindEvents();
        },

        _bindEvents: function() {
            this.audio.onloadeddata = function(){
                VoiceKit.audio.play();
            };
            this.audio.onended = function(){
                VoiceKit.endSoundHandler();
            };
            this.switcher.on('change', function() {
                localStorage.setItem('chat-voice-switcher', VoiceKit.isSwitchOn());
                VoiceKit.checkPlay();
            });
        },

        play: function(){
            this.isBusy = true;
            this.currentIndex++;
            this.audio.src = 'https://tts.voicetech.yandex.net/generate?' +
                'key=2308bf65-4316-45e9-bcec-0f9d86a7ab63' +
                '&text=' + encodeURI(this.queue[this.currentIndex]) +
                '&fornat=wav' +
                '&lang=ru-RU' +
                '&speaker=jane';
            this.audio.load();
        },

        endSoundHandler: function(){
            this.isBusy = false;
            this.checkPlay();
        },

        checkPlay: function (){
            if ( this.isSwitchOn() && !this.isBusy && !this.isQueueEnded()  ){
                this.play();
            }
        },

        addQueueItem: function(text){
            this.queue.push(text);
            this.checkPlay();
        },

        isSwitchOn: function() {
            return this.switcher.is(':checked');
        },

        isQueueEnded: function(){
            return this.queue.length === (this.currentIndex + 1);
        }
    };
    VoiceKit.init();
});