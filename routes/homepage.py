from flask import render_template, Blueprint
import configparser
from utilities.featured_species import featured_species_function

# config = configparser.ConfigParser()

page = Blueprint("home", __name__, url_prefix="/")


@page.route("/")
def home():
    featured_species = featured_species_function('config.ini')
    return render_template(
        "home/home.jinja",
        featured_species=featured_species
        )
