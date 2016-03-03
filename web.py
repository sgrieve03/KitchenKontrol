# flask
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user


# python
import json

# application

login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


app.debug = True
app.use_reloader = True

crsf = CsrfProtect()
crsf.init_app(app)


from flask import render_template, request
from flask import url_for, redirect




# visible  web pages
@app.route("/")
@app.route("/index")
def index():
    pass

import auth.forms
import auth.models
# protected web pages

@app.route("/register", methods=["GET", "POST"])
def register():
    errors = request.args.get('errors', [])
    if errors:
        errors = json.loads(errors)

    form = auth.forms.NewUser()

    if request.method == 'GET':
        return (render_template('register.html', form=form, errors=errors))
    
    if not form.validate():
        return (render_template('register.html', form=form, errors=errors))
  
    

    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = request.args.get('errors', [])
    if errors:
        errors = json.loads(errors)

    form = auth.forms.LoginForm()

    if request.method == 'GET':
        return (render_template('login.html', form=form, errors=errors))

    if not form.validate():
        return (render_template('login.html', form=form, errors=errors))

    
    username = request.form['username']
    registered_user = auth.models.User.query.\
        filter_by(username=username).first()
    remember_me = False
    if 'remember' in request.form:
        remember_me = True
    print remember_me
    login_user(registered_user, remember=remember_me)    
    
    return redirect(request.args.get('next') or url_for('home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


@app.route("/home")
def home():
        return render_template('home.html')


@app.route("/food")
def food():
    return render_template("food.html")

@app.route("/sanitation")
@login_required
def sanitation():
    return render_template("sanitation.html")


@app.route("/devices")
@login_required
def device():
    return render_template("devices.html")


@app.route("/inspection")
def inspection():
    return render_template("inspection.html")


@app.route("/manager")
@login_required
def manager():
    return render_template("manager.html")


@login_manager.user_loader
def load_user(user_id):
    u = auth.models.User.query.filter_by(id=user_id).first()
    if u:
        print u.__repr__
        return u
    else:
        return None

if __name__ == "__main__":
    # start flask 
    app.run(host='0.0.0.0', port=5050)



