from flask import render_template, Blueprint, request
import configparser

from database.db_commands import get_all_species, search_species

config = configparser.ConfigParser()

page = Blueprint("species", __name__, url_prefix="/species")

@page.route("")
def all_species():
    config.read('config.ini')
    
    featured_species = list(dict(config["homepage"]).values())

    species_list = get_all_species()
        
    species_list = sorted(species_list, key=lambda sp: sp['species_english'])
    
    for sp in species_list:
        print(sp['species_english'])

    return render_template(
        "species/species.jinja",
        species=species_list,
        featured_species=featured_species
        )
    
@page.route("/search")
def search():
    query = request.args.get("search-query")

    results = search_species(query)
    
    return render_template("/species/species_search.jinja", results=results, query=query)