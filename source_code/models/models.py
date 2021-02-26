from source_code.database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(55), unique=True)
    password = db.Column(db.String(85))
    firstname = db.Column(db.String(55))
    lastname = db.Column(db.String(55))
    bio = db.Column(db.String(510))
    followers = db.Column(db.Text())
    following = db.Column(db.Text())

    # def __init__(self, username, email, password):
    #     self.username = username
    #     self.email = email
    #     self.password = password

    def __repr__(self):
        return f'<User {self.username}>'


class PyTweet(db.Model):
    __tablename__ = 'pytweets'

    tweet_id = db.Column(db.Integer, primary_key=True, unique=True)
    from_user_id = db.Column(db.Integer)
    tweet = db.Column(db.String(310))
    datetime_created = db.Column(db.String(50))  # format: MM-DD-YYYY hh:mm:ss AM/PM

    def __repr__(self):
        return f'<PyTweet id={self.tweet_if} from_user={self.from_user_id} tweet_data={self.datatime_created}>'
