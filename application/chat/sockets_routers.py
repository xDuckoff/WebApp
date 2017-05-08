def create_routers(socketio):
    from application import app
    from application import chat
    from flask import session
    if app.config['SOCKET_MODE'] == 'True':
        from flask_socketio import emit, join_room, leave_room

        @socketio.on('message')
        def handle_message(json):
            chat_id = int(json['room'])
            if len(json['message']) > 1000:
                return
            chat.send_message(chat_id, json['message'], 'usr', session['login'])
            socketio.emit('message', {'message':json['message'], 'author':session['login'], 'type':'usr'}, json=True, room=json['room'], broadcast=True)

        @socketio.on('join')
        def on_join(room):
            join_room(room)
            chat.sys_message(str(session['login']) + " joined", room)

        @socketio.on('leave')
        def on_leave(room):
            leave_room(room)

    if app.config['SOCKET_MODE'] == 'False':
        from application import chat
        from application.forms import IsInSession
        from flask import redirect, request, session
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