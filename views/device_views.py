# flask
from flask import request, render_template
from flask.ext.login import login_required
import flask.ext.login as f

# application
import auth.forms
import auth.models
from db import device, delivery
from auth_views import app

c_u = f.current_user


@app.route("/appliance", methods=["GET", "POST"])
@login_required
def appliance():
    devices = device.get_devices()
    thermometers = delivery.get_thermometers()
    context = {'devices': devices,
            'thermometers': thermometers}

    form = auth.forms.AlertForm()
    return render_template("appliance.html", form=form, **context)
