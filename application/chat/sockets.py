from application import app

def check_mode():
	if app.config['SOCKET_MODE'] == 'True':
	    from application import socketio
	    from flask_socketio import emit
	return app.config['SOCKET_MODE'] == 'True'

def send_code_sockets(id):
    if check_mode():
        socketio.emit('commit', room=str(id), broadcast=True)

def sys_message_sockets(data, room):
    if check_mode():
        socketio.emit('message', {'message':data, 'author':'System', 'type':'sys'}, room=room, broadcast=True)