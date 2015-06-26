# -*- coding: utf-8 -*-
"""
    Voyage Application package
"""

from flask import Flask
voyage_app = Flask(__name__)

@voyage_app.route("/")
def hello():
    return "<h1>Hello There!</h1>"
