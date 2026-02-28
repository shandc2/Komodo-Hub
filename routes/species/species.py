from flask import render_template, Blueprint
import configparser

from database.db_commands import get_all_species

config = configparser.ConfigParser()

page = Blueprint("species", __name__)

@page.route("/species")
def all_species():
    config.read('config.ini')
    
    featured_species = list(dict(config["homepage"]).values())

    species_list = get_all_species()
    
    for sp in species_list:
        print(sp['species_english'])

    return render_template(
        "species/species.jinja",
        species=species_list,
        featured_species=featured_species
        )