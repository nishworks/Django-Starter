# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_admin import Admin

from voyage.api import rest_api
from voyage.config import Config

#Setup app
app = Flask(__name__, template_folder=Config.TEMPLATES_FOLDER)
app.config.from_object(Config)


#Blueprints
app.register_blueprint(rest_api)

#Setup admin
#voyage_admin = Admin(voyage_app, name='Voyage')

@app.route("/")
def index():
    return render_template('base.html', title="Base page")



