from flask import render_template, Blueprint
from database.db_commands import get_species_by_name
import sqlite3

page = Blueprint("species_information", __name__)


# animal_from_database expects five variables:
# id, english_name, latin_name, body_text and
# if this needs changing feel free to adjust but...
# species_information.jinja does expect english_name, latin_name and main_text
# this page works by taking the "species_id" from the url and using that to
# read the database.
# Because of this we are able to create one page and simply generate links
# based on the contents of the database
# i.e. we can create a button with the hyperlink /species/iguana and this will
# allow the user to view the information about the species
# please be aware the page expects a .jpg at:
# /static/images/species_database/{{species_id}}.jpg


@page.route("/species/<species_english>")
def data(species_english):
    try:
        database_entry = get_species_by_name(species_english)
        # print(dict(database_entry))
        return render_template(
            "species_information/species_information.jinja",
            english_name=database_entry["species_english"],
            latin_name=database_entry["species_latin"],
            main_text=database_entry["body_text"],
            category=database_entry["category"],
            extinction_risk=database_entry["extinction_risk"],
            )
    except TypeError as error_information:
        return render_template(
            "error.jinja",
            extra_information=error_information,
            )
