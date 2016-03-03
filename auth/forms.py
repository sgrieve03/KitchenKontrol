from models import User
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class NewUser(Form):
    user_id = 1
    username = TextField('username', [DataRequired('Must provide a username')])
    password = TextField('password', [DataRequired('Must provide a password')])
    email = TextField('email', [DataRequired('Must provide an email address')])

    def validate(self):
        if not Form.validate(self):
            print 'Invalid!'
            return False
        print 'Valid!'

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            return False
        else:
            self.user_id +=1
            return True



class LoginForm(Form):
    username = TextField('username',
        [DataRequired('Must provide a username/password')])
    password = PasswordField('password',
        [DataRequired('Must provide a username/password')])
    remember_me = BooleanField('remember_me')

    def validate(self):
        if not Form.validate(self):
            print 'Invalid!'
            return False
        print 'Valid!'

        user = User.query.filter_by(username=self.username.data).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            return False
