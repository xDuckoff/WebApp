from application import app
from application import chat
from flask import redirect, request, session
from application.forms import IsInSession
def create_routers(socketio):
    if app.config['SOCKET_MODE'] == 'True':
        from flask_socketio import join_room, emit, leave_room
        """
        Данный файл содержит функции и страницы сокетов и чата
        """
        @socketio.on('message')
        def handle_message(json):
            """
            **Работает только с сокетами**
            Данная функция принимает сообщения от пользователя
            
            :param json: json запрос
            
            :return: Сообщние
            """
            chat_id = int(json['room'])
            if len(json['message']) > 1000:
                return
            chat_id = int(json['room'])
            message = cgi.escape(json['message'])
            message = markdown.markdown(message)
            chat.send_message(chat_id, message, 'usr', session['login'])
            socketio.emit('message', {'message':message, 'author':session['login'], 'type':'usr'}, json=True, room=json['room'], broadcast=True)

        @socketio.on('join')
        def on_join(room):
            """
            **Работает только с сокетами**
            Данная функция сообщает о присоединение пользователя к чату
            
            :param room: номер чата
            
            :return: Системное сообщение о входе пользователя
            """
            join_room(room)
            if room not in session['joined_chats']:
                chat.sys_message(str(session['login']) + " joined", room)


        @socketio.on('leave')
        def on_leave(room):
            """
            **Работает только с сокетами**
            Данная функция удаляет человека из чата
            
            :param room: Номер чата
            """
            leave_room(room)

    if app.config['SOCKET_MODE'] == 'False':
        @app.route('/send_message', methods=['GET', 'POST'])
        def send_message():
            if not(IsInSession()):
                return redirect('/login')
            chat_id = int(request.args['chat'])
            message = request.args['message']
            if len(message) > 1000:
                return 'LENGTH LIMIT'
            if len(message) > 0:
                chat.send_message(chat_id, message, "usr", session['login'])
            return 'OK'