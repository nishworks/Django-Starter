# -*- coding: utf-8 -*-

from flask import Flask, render_template
from voyage.api import rest_api
from voyage import config

#Setup app
voyage_app = Flask(__name__)
voyage_app.config.from_object(config)
voyage_app.logger.info("nishant")

#Blueprints
voyage_app.register_blueprint(rest_api)

@voyage_app.route("/")
def index():
    voyage_app.logger.info("nishant")
    return render_template('base.html', title="Base page")



