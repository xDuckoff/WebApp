# -*- coding: utf-8 -*-

from application import app

socketio = None


def init_sockets():
    global socketio
    from sockets_routers import create_routers
    if app.config['SOCKET_MODE'] == 'True':
        from flask_socketio import SocketIO
        socketio = SocketIO(app)
    create_routers(socketio)
    return app.config['SOCKET_MODE'] == 'True'


def send_code_sockets(id):
    if app.config['SOCKET_MODE'] == 'True':
        socketio.emit('commit', room=str(id), broadcast=True)


def sys_message_sockets(data, room):
    if app.config['SOCKET_MODE'] == 'True':
        socketio.emit('message', {'message': data, 'author': u'Системное сообщение', 'type': 'sys'}, room=room, broadcast=True)
