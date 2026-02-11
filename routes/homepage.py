from flask import render_template, request, Blueprint
from routes.donation.donation import donation_page

home_page = Blueprint('home', __name__, url_prefix='/')
home_page.register_blueprint(donation_page)

@home_page.route('/')
def home():
    return render_template('home/home.jinja')