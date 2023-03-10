from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Kanban(db.Model):
    __tablename__ = 'kanban'
    public_id = db.Column(db.String(50), unique = True, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))
    is_done = db.Column(db.Boolean, default=False)

    def __init__(self,public_id, title, content, is_done):
            self.public_id = public_id
            self.title= title
            self.content=content
            self.is_done = is_done

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(255))
