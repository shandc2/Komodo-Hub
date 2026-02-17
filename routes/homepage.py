from flask import render_template, Blueprint
from routes.donation.donation import donation_page
from routes.species_info.species_info import species_info_page
from routes.error.error import error_page
from routes.species_portal.species_portal import species_portal

home_page = Blueprint("home", __name__, url_prefix="/")
home_page.register_blueprint(donation_page)
home_page.register_blueprint(species_info_page)
home_page.register_blueprint(error_page)
home_page.register_blueprint(species_portal)



@home_page.route("/")
def home():
    return render_template("home/home.jinja")
