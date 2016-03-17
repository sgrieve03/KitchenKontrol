# flask
from flask.ext.login import login_required
# python
import json

# application
import auth.forms
import auth.models
from db import delivery


from flask import render_template, request


from auth_views import app


@app.route("/orders", methods=["GET", "POST"])
@login_required
def orders():
    form = auth.forms.AlertForm()
    suppliers = delivery.get_suppliers()
    overview = delivery.get_overview()
    appliances = delivery.get_appliances()
    thermometers = delivery.get_thermometers()
    todays_suppliers = delivery.get_todays_suppliers()
    context = {"suppliers": suppliers,
            "overview": overview,
            "appliance": appliances,
            "todays_suppliers": todays_suppliers,
            "thermometers": thermometers}
    return render_template("orders.html", form=form, **context)


@app.route("/orders/enter")
def enter():
    from auth_views import current_user
    business_name = request.args.get('business_name')
    invoice = request.args.get("invoice")
    item = request.args.get('item')
    qty = request.args.get('qty')
    temp = request.args.get('temp')
    therm = request.args.get('therm')
    ubd = request.args.get('ubd')
    dest = request.args.get("dest")
    comment = request.args.get('status')
    supplier_id = request.args.get('supplier_id')

    if business_name is not None:
        delivery.start_new_delivery(business_name, invoice)
        delivery.add_delivered_item(business_name, invoice, ubd, item, temp, 
                dest, therm, qty, comment, current_user)
    else:
        delivery.add_delivered_item(supplier_id, invoice, ubd, item, temp, dest,
                therm, qty, comment, current_user)
    success = {"true": True}
    return json.dumps(success)


@app.route("/suppliersItems")
@login_required
def suppliersItems():
    a = request.args.get('a')
    items = delivery.get_items(a)
    print items
    return json.dumps(items)
