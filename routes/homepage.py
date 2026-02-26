from flask import render_template, Blueprint
import configparser

config = configparser.ConfigParser()

page = Blueprint("home", __name__, url_prefix="/")


@page.route("/")
def home():
    config.read('config.ini')
    species1 = config['homepage']['featured_species_1']
    species2 = config['homepage']['featured_species_2']
    species3 = config['homepage']['featured_species_3']
    print(f'Featured species: {species1}, {species2}, {species3}')
    return render_template(
        "home/home.jinja",
        species_list=list(dict(config['homepage']).values())
        )
