from application import app

socketio = 0

def check_mode():
	if app.config['SOCKET_MODE'] == 'True':
		from flask_socketio import SocketIO
		socketio = SocketIO(app)
		from flask_socketio import emit
		from sockets_routers import create_routers
		create_routers(socketio)
	return app.config['SOCKET_MODE'] == 'True'

def send_code_sockets(id):
    if check_mode():
        socketio.emit('commit', room=str(id), broadcast=True)

def sys_message_sockets(data, room):
    if check_mode():
        socketio.emit('message', {'message':data, 'author':'System', 'type':'sys'}, room=room, broadcast=True)