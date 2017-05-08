from application import app
if app.config['SOCKET_MODE'] == 'True':
    
    from flask_socketio import emit

def send_code_sockets(id):
    if app.config['SOCKET_MODE'] == 'True':
    	from application import socketio
        socketio.emit('commit', room=str(id), broadcast=True)

def sys_message_sockets(data, room):
    if app.config['SOCKET_MODE'] == 'True':
    	from application import socketio
        socketio.emit('message', {'message':data, 'author':'System', 'type':'sys'}, room=room, broadcast=True)