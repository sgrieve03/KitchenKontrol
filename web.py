# flask
from collections import OrderedDict
from flask import Flask, render_template, request, Response

# python
import threading
import time
import datetime
import sys
import signal, os
from pprint import pprint
import json


app = Flask(__name__)
app.debug = True
app.use_reloader = True

# web pages

@app.login("/login")
def index():
    return render_template('login.html')

@app.route("/home")
def index():
        return render_template('home.html')

@app.route("/food")
def food():
    return render_template("food.html")

@app.route("/sanitation")
def sanitation():
    return render_template("sanitation.html")

@app.route("/devices")
def device():
    return render_template("devices.html")






# start flask 
app.run(host='0.0.0.0', port=5050)



