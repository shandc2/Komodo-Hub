from flask import render_template, Blueprint
import configparser

config = configparser.ConfigParser()

page = Blueprint("home", __name__, url_prefix="/")


@page.route("/")
def home():
    config.read('config.ini')
    featured_species = list(dict(config["homepage"]).values())
    # print(f'Featured species: {species1}, {species2}, {species3}')
    return render_template(
        "home/home.jinja",
        featured_species=featured_species
        )
