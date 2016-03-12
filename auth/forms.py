from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField,\
    validators, fields 
from wtforms.validators import DataRequired
from db import login, register, forgotpswd, sanitation
from web import todays_cleaning, todays_pest


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

    def senddb(self, ref_type, location, comment, userid):
        sanitation.create_check(ref_type, location, comment, userid)        

    def save(self, ref_type, location, day, description):
        sanitation.create_strategy(ref_type, location, description, day)


class PestForm(Form):
    areas = todays_pest
    location = fields.SelectMultipleField('location', todays_pest)
    topic = fields.SelectField('topic', 
            choices=['Broken/damaged Trap', "Low Poison Supplies"])
    comment = fields.TextAreaField(u'comment', 
            [validators.optional(), validators.length(max=220)])

    def senddb(self, ref_type, location, comment, userid):
        sanitation.create_check(ref_type, location, comment, userid)        

    def save(self, ref_type, location, day, description):
        sanitation.create_strategy(ref_type, location, description, day)
