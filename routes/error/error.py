from flask import render_template, Blueprint

page = Blueprint('error', __name__, url_prefix='/error')


@page.route('/')
def error():
    return render_template('error.jinja')