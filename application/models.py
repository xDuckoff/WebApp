from application import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256))
    author = db.Column(db.String(256))
    chat = db.Column(db.Integer)

    def __init__(self, content, author, chat):
        self.content = content
        self.author = author
        self.chat = chat
