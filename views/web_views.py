# flask
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask.ext.mail import Mail, Message
from flask.ext.login import LoginManager, login_user,\
    logout_user, login_required
from flask import render_template, request
from flask import url_for, redirect

# python
import json, os, jinja2
import config

# application
import auth.forms
import auth.models


app = Flask(__name__)
login_manager = LoginManager()
app.config.from_object('config')
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

app.debug = True
app.use_reloader = True

crsf = CsrfProtect()
crsf.init_app(app)


# visible  web pages
@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    form = auth.forms.ForgotPasswordForm()
    if request.method == "GET":
        return render_template("forgotpassword.html", form=form)
    if not form.validate():
        return render_template("forgotpassword.html", form=form)
    else:
        password = form.newpassword
        msg = Message("New Password", 
                sender=config.MAIL_USERNAME,
                recipients=[form.email.data])
        msg.body = "Your new Kitchen Kontrol password is: "\
            + password + "\n\n\n"

        mail.send(msg)
        return redirect(url_for('login'))


@app.route("/inspection")
def inspection():
    return render_template("inspection.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = auth.forms.NewUser()
    if request.method == 'GET':
        return (render_template('register.html', form=form))
    if not form.validate():
        return (render_template('register.html', form=form))
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = request.args.get('errors', [])
    if errors:
        errors = json.loads(errors)
    form = auth.forms.LoginForm()
    if request.method == 'GET':
        return (render_template('login.html',
            form=form, errors=errors))
    if not form.validate():
        return (render_template('login.html',
            form=form, errors=errors))
    email = request.form['email']
    global current_email
    current_email = email
    print current_email
    registered_user = auth.models.User(email=email)
    remember_me = False
    if 'remember' in request.form:
        remember_me = True
    login_user(registered_user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('home'))


# protected web pages
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


@app.route("/food")
@login_required
def food():
    return render_template("food.html")


@app.route("/devices")
@login_required
def device():
    return render_template("devices.html")


@login_manager.user_loader
def load_user(user_id):
    u = auth.models.User(user_id)
    global current_user
    current_user = user_id
    print user_id
    if u:
        return u
    else:
        return None 

from views.order_views import *
from views.sanitation_views import *
from views.home_views import *

static = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.jinja_loader = jinja2.FileSystemLoader(static)
template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app.jinja_loader = jinja2.FileSystemLoader(template)


