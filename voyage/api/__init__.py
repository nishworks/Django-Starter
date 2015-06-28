from flask import Blueprint, render_template

rest_api = Blueprint('simple_page', __name__)

@rest_api.route('/<page>')
def show(page):
    return render_template('base.html', title="API Blueprint")