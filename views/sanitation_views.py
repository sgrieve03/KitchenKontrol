# flask
from flask import request, render_template
from flask.ext.login import login_required

# python
import config

# application
import auth.forms
import auth.models
from db import sanitation
from auth_views import app, mail, Message


@app.route("/sanitation", methods=["GET", "POST"])
@login_required
def sanitize():
    from auth_views import current_email, current_user
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


@app.route("/pest", methods=["GET", "POST"])
@login_required
def pest():
    from auth_views import current_email, current_user
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
