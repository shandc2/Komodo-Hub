from flask import render_template, Blueprint

donation_page = Blueprint('donation', __name__, url_prefix='/donation')


@donation_page.route('/')
def home():
    return render_template('donation/donation.jinja')