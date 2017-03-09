from application import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(256))
    chat = db.Column(db.Integer)

    def __init__(self, content, author, chat):
        self.content = content
        self.author = author
        self.chat = chat


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    author = db.Column(db.String(256))
    chat = db.Column(db.Integer)

    def __init__(self, content, author, chat):
        self.content = content
        self.author = author
        self.chat = chat


class Chat_Model(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))

    def __init__(self, id, name):
        self.id = id
        self.name = name
