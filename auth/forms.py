from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField,\
    validators, fields 
from wtforms.validators import DataRequired
from db import login, register, forgotpswd, cleaning
from web import todays_cleaning


class NewUser(Form):
    firstname = TextField('Username', 
            [validators.Length(min=4, max=20)])
    lastname = TextField('Username', 
            [validators.Length(min=4, max=20)])
    email = TextField('Email Address', 
            [DataRequired('Must provide an email address')])
    password = PasswordField('New Password', 
            [validators.Required(),
            validators.EqualTo('password2', 
            message='Passwords must match')])
    password2 = PasswordField('Repeat Password')

    def validate(self):
        if not Form.validate(self):
            print 'Invalid!'
            return False
        print 'Valid!'
        user = register.validate(self.firstname.data, 
            self.lastname.data, self.email.data, self.password.data)
        if user:
            return True 
        else:
            return False


class LoginForm(Form):
    email = TextField('email',
        [DataRequired('Must provide a username/password')])
    password = PasswordField('password',
        [DataRequired('Must provide a username/password')])
    remember_me = BooleanField('remember_me')

    def validate(self):
        if not Form.validate(self):
            print 'Invalid!'
            return False
        print 'Valid!'
     
        v = login.check_password()
        if v.validate(self.password.data, self.email.data):
            print "exists"
            return True
        else:
            print "doeesnt exist"
            return False


class ForgotPasswordForm(Form):
    email = TextField('email',
            [DataRequired('Must provide an email')])
    newpassword = ""
    
    def validate(self):
        if not Form.validate(self):
            print 'Invalid!'
            return False
        print 'Valid!'
        
        m = forgotpswd.send()
        self.newpassword = m.validate(self.email.data)
        return True


class AlertForm(Form):
    areas = todays_cleaning
    location = fields.SelectMultipleField('location', todays_cleaning)
    topic = fields.SelectField('topic', 
            choices=['Broken/damaged Item', "Low Cleaning Supplies"])
    comment = fields.TextAreaField(u'comment', 
            [validators.optional(), validators.length(max=220)])

    def senddb(location, comment, id):
        cleaning.create_check(location, comment, id)        

    def save(location, day, description):
        cleaning.create_cleaning_strategy(location, description, day)
