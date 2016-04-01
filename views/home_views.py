# flask
import flask.ext.login
from flask import request
from flask.ext.login import login_required
from flask import render_template

# python
import json
import config

# application
from db import sanitation, delivery, user
from auth_views import app
import auth.forms
c_u = flask.ext.login.current_user


@app.route("/")
@app.route("/index")
def index():
    pass


@app.route('/home/charts')
@login_required
def chart():
    activities = user.get_user_stat(c_u.user_id)
    contract = user.get_user_contract(c_u.user_id)
    data = []
    if contract == 'P':
        aim = {'Cleaning': 15, 'Pest': 5, 'Temperature': 10}
    else:
        aim = {'Cleaning': 22, 'Pest': 8, 'Temperature': 25}
    for k, v in activities.items():
        data.append({"stat": k, "value": v, "aim": aim[k]})
    return json.dumps(data)


@app.route("/home/notes", methods=["GET"])
@login_required
def notes():
    a = request.args.get('a')
    if a:
        result = user.set_notes(c_u.user_id, a)
        return json.dumps({"result": result})
    else:
        notes = user.get_notes(c_u.user_id)
        if notes:
            return json.dumps(notes)
        else:
            return json.dumps("No notes to display")


@app.route("/home")
@login_required
def home():
    form = auth.forms.AlertForm()
    cleaningcount = sanitation.get_count_remaining_tasks(config.cleaning)
    pestcount = sanitation.get_count_remaining_tasks(config.pest)
    suppliers = delivery.get_todays_suppliers()
    context = {"cleaningcount": cleaningcount,
               "pestcount": pestcount,
               "suppliers": suppliers}
    return render_template('landingpage.html', form=form, **context)
