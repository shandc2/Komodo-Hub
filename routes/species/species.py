from flask import render_template, Blueprint, request
import configparser

from database.db_commands import get_all_species, search_species, get_species_by_name
from utilities.featured_species import featured_species_function

config = configparser.ConfigParser()

page = Blueprint("species", __name__, url_prefix="/species")

# species database page
@page.route("")
def all_species():    
    featured_species = featured_species_function('config.ini')

    species_list = get_all_species()
        
    species_list = sorted(species_list, key=lambda sp: sp['species_english'])
    
    for sp in species_list:
        print(sp['species_english'])

    return render_template(
        "species/species.jinja",
        species=species_list,
        featured_species=featured_species
        )
    
# search page
@page.route("/search")
def search():
    query = request.args.get("search-query")

    results = search_species(query)
    print(results)
    return render_template("/species/species_search.jinja", results=results, query=query)