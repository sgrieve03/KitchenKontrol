# flask
from flask.ext.login import login_required
# python
import json
import config

# application
from db import sanitation, delivery, user
from flask import render_template
from auth_views import app


@app.route("/")
@app.route("/index")
def index():
    pass


@app.route('/home/charts')
@login_required
def chart():
    from auth_views import current_user
    print current_user
    activities = user.get_user_stat(current_user)
    data = []
    aim = {'Cleaning': 15, 'Pest': 5, 'Temperature': 10}
    for k, v in activities.items():
        data.append({"stat": k, "value": v, "aim": aim[k]})
    return json.dumps(data)


@app.route("/home")
@login_required
def home():
    cleaningcount = sanitation.get_count_remaining_tasks(config.cleaning)
    pestcount = sanitation.get_count_remaining_tasks(config.pest)
    suppliers = delivery.get_todays_suppliers()
    context = {"cleaningcount": cleaningcount,
               "pestcount": pestcount,
               "suppliers": suppliers}
    return render_template('landingpage.html', **context)
