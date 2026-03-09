from flask import render_template, Blueprint
from database.db_commands import get_species_by_name
import sqlite3

page = Blueprint("species_information", __name__)

# this page works by taking the species name (in english) from the url and using that to read the database.
# Because of this we are able to create one page and simply generate links based on the contents of the database
# i.e. we can create a button with the hyperlink /species/iguana and this will
# allow the user to view the information about the species
# please be aware the page expects a .jpg at:
# /static/images/species_database/{{photoid}}.jpg but this will be generated automatically
# so long as you use the species_portal or species editor pages I created - CS


@page.route("/species/<species_english>")
def data(species_english):
    try:
        database_entry = get_species_by_name(species_english)
        if database_entry is None:
            raise TypeError(f"No species named '{species_english}' found in the database.")
        return render_template(
            "species_information/species_information.jinja",
            english_name    =(database_entry["species_english"]).capitalize(),
            latin_name      =database_entry["species_latin"].capitalize(),
            main_text       =database_entry["body_text"],
            category        =database_entry["category"].capitalize(),
            extinction_risk =database_entry["extinction_risk"],
            photoid         =database_entry["photoid"],
            species_id      =str(database_entry["species_id"])
        )
    except TypeError as error_information:
        return render_template(
            "error.jinja",
            extra_information=error_information,
        )
