from flask import render_template, Blueprint

page = Blueprint('donation', __name__, url_prefix='/donation')


@page.route('/')
def home():
    return render_template('donation/donation.jinja')