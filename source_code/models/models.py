from source_code.database import db


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(55), unique=True)
    password =db.Column(db.String(85))

    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password

    def __repr__(self):
        return f'<User {self.username}>'
