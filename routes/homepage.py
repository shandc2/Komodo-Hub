from flask import render_template, Blueprint
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

species1 = config['homepage']['featured_species_1']
species2 = config['homepage']['featured_species_2']
species3 = config['homepage']['featured_species_3']

print(f'Featured species: {species1}, {species2}, {species3}')

page = Blueprint("home", __name__, url_prefix="/")


@page.route("/")
def home():
    return render_template(
        "home/home.jinja",
        species1=species1,
        species2=species2,
        species3=species3,
        )
