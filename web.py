# flask
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask.ext.mail import Mail, Message

from flask_login import LoginManager, login_required, login_user, logout_user

# python
import json
import config

# application
import auth.forms
import auth.models
from db import sanitation

login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object('config')

login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

app.debug = True
app.use_reloader = True

crsf = CsrfProtect()
crsf.init_app(app)


from flask import render_template, request
from flask import url_for, redirect

todays_cleaning = sanitation.get_todays_tasks(config.cleaning)
overview = sanitation.get_overview(config.cleaning)

todays_pest = sanitation.get_todays_tasks(config.pest)
pest_overview = sanitation.get_overview(config.pest)

current_email = ""
current_user = ""


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


@app.route("/sanitation", methods=["GET", "POST"])
@login_required
def sanitize():
    todays_cleaning = sanitation.get_todays_tasks(config.cleaning)
    overview = sanitation.get_overview(config.cleaning)
    context = {'todays_cleaning': todays_cleaning,
            'overview': overview}
    form = auth.forms.AlertForm()
    if request.method == "POST":
        if request.form['buttons'] == 'send':
            location = request.form['location']
            topic = request.form['topic']
            comment = request.form['comment']
            msgtosend = comment + " From " + current_email
            msg = Message(location + ": " + topic,
                    sender=config.MAIL_USERNAME,
                    recipients=[config.MAIL_USERNAME])
            msg.body = msgtosend
            mail.send(msg)
            userid = current_user
            if topic == 'Complete':
                form.senddb(config.cleaning, location, comment, userid)
                todays_cleaning = sanitation.get_todays_tasks(config.cleaning)
                overview = sanitation.get_overview(config.cleaning)
                context = {'todays_cleaning': todays_cleaning,
                    'overview': overview}
        if request.form['buttons'] == 'save':
            location = request.form['location']
            days = request.form.getlist('day')
            d = []
            for day in days:
                d.append(int(day))
            description = request.form['description']
            form.save(config.cleaning, location, d, description)
            todays_cleaning = sanitation.get_todays_tasks(config.cleaning)
            overview = sanitation.get_overview(config.cleaning)
            context = {'todays_cleaning': todays_cleaning,
                'overview': overview}
    return render_template("cleaning.html", form=form, **context)


@app.route("/")
@app.route("/index")
def index():
    pass


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


@app.route("/home")
@login_required
def home():
        return render_template('landingpage.html')


@app.route("/food")
@login_required
def food():
    return render_template("food.html")


@app.route("/devices")
@login_required
def device():
    return render_template("devices.html")


@app.route("/pest", methods=["GET", "POST"])
@login_required
def pest():
    todays_pest = sanitation.get_todays_tasks(config.pest)
    pest_overview = sanitation.get_overview(config.pest)
    context = {'todays_pest': todays_pest,
            'overview': pest_overview}
    form = auth.forms.AlertForm()
    if request.method == "POST":
        if request.form['buttons'] == 'send':
            location = request.form['location']
            topic = request.form['topic']
            comment = request.form['comment']
            msgtosend = comment + " From " + current_email
            msg = Message(location + ": " + topic,
                    sender=config.MAIL_USERNAME,
                    recipients=[config.MAIL_USERNAME])
            msg.body = msgtosend
            mail.send(msg)
            userid = current_user
            if topic == 'Complete':
                form.senddb(config.pest, location, comment, userid)
                todays_pest = sanitation.get_todays_tasks(config.pest)
                overview = sanitation.get_overview(config.pest)
                context = {'todays_pest': todays_pest,
                    'overview': overview}
        if request.form['buttons'] == 'save':
            location = request.form['location']
            days = request.form.getlist('day')
            d = []
            for day in days:
                d.append(int(day))
            description = request.form['description']
            form.save(config.pest, location, d, description)
            todays_pest = sanitation.get_todays_tasks(config.pest)
            overview = sanitation.get_overview(config.pest)
            context = {'todays_pest': todays_pest,
                'overview': overview}
    return render_template("pest.html", form=form, **context)


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


if __name__ == '__main__':
    # start flask 
    app.run(host='0.0.0.0', port=5050)



