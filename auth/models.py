from werkzeug.security import generate_password_hash, \
    check_password_hash
from web import db

class User(db.Model):
    __tablename__ = "User"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(128))
    email = db.Column('email', db.String(50), unique=True, index=True)

    def __init__(self, username="", password="", email=""):
        self.username = username
        self.set_password(password)
        self.email = email
    
    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
