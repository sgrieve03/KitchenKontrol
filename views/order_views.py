# flask
from flask.ext.login import login_required
import flask.ext.login
from flask import render_template, request

# python
import json

# application
import auth.forms
import auth.models
from db import delivery
from auth_views import app


c_u = flask.ext.login.current_user


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


@app.route("/orders/addSupplier")
@login_required
def add_supplier():

    bname = request.args.get('bname')
    stele = request.args.get('stele')
    atele = request.args.get('atele')
    fline = request.args.get('first_line')
    sline = request.args.get('second_line')
    tline = request.args.get('third_line')
    town = request.args.get('town')
    pcode = request.args.get('postcode')
    success = delivery.add_supplier(bname, stele, atele, fline, sline,
        tline, town, pcode)
    return json.dumps({"success": success})


@app.route("/orders/enter")
def enter():
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
                dest, therm, qty, comment, c_u.user_id)
    else:
        delivery.add_delivered_item(supplier_id, invoice, ubd, item, temp, dest,
                therm, qty, comment, c_u.user_id)
    success = {"true": True}
    return json.dumps(success)


@app.route("/orders/addtoitems")
def addtoitems():
    business_name = request.args.get('business_name')
    invoice = request.args.get("invoice")
    item = request.args.get('item')
    qty = request.args.get('qty')
    temp = request.args.get('temp')
    therm = request.args.get('therm')
    ubd = request.args.get('ubd')
    dest = request.args.get("dest")
    comment = request.args.get('status')

    delivery.add_delivered_item(business_name, invoice, ubd, item,
        temp, dest, therm, qty, comment, c_u.user_id)
    success = {"true": True}
    return json.dumps(success)


@app.route("/orders/update")
def update():
    business_name = request.args.get('business_name')
    invoice = request.args.get("invoice")
    item = request.args.get('item')
    qty = request.args.get('qty')
    temp = request.args.get('temp')
    therm = request.args.get('therm')
    ubd = request.args.get('ubd')
    dest = request.args.get("dest")
    comment = request.args.get('status')

    delivery.update_delivered_item(business_name, invoice, ubd, item,
        temp, dest, therm, qty, comment, c_u.user_id)
    success = {"true": True}
    return json.dumps(success)


@app.route("/suppliersItems")
@login_required
def suppliersItems():
    a = request.args.get('a')
    items = delivery.get_items(a)
    return json.dumps(items)


@app.route("/checkInvoice")
def checkInvoice():
    num = request.args.get('a')
    duplicate = delivery.checkInvoice(num)
    duplicate = {"duplicate": duplicate}
    return json.dumps(duplicate)


@app.route("/orders/add")
def add():
    items = []
    a = request.args.get('a')
    item = delivery.get_items(a)
    for k, v in item.items():
        items.append({"item": v})
    invoice = delivery.get_order_invoice(a)
    items.append({"invoice": invoice})
    return json.dumps(items)


@app.route("/orders/edit")
def edit():
    items = []
    a = request.args.get('a')
    invoice = delivery.get_order_invoice(a)
    item = delivery.get_edit_items(invoice)
    for k, v in item.items():
        items.append({"item": v})
    items.append({"invoice": invoice})
    return json.dumps(items)


@app.route("/loaditem")
def loaditem():
    a = request.args.get('item')
    b = request.args.get('invoice')
    item = delivery.loaditem(a, b)
    return json.dumps(item)


