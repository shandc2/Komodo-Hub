from flask import render_template, Blueprint

page = Blueprint('about', __name__, url_prefix='/about')


@page.route('')
def home():
    return render_template('about/about.jinja')