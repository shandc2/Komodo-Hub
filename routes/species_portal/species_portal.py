from flask import render_template, Blueprint, request
from database.db_commands import add_species
import os

page = Blueprint("species_portal", __name__, url_prefix="/species/portal")


@page.route("/")
def portal():
    return render_template("species_portal/species_portal.jinja")


@page.route("/", methods=["POST"])
def add_species_to_database():
    try:
        eng_name        = request.form["eng_name"]
        latin_name      = request.form["latin_name"]
        main_text       = request.form["main_text"]
        category        = request.form["category"]
        extinction_risk = request.form["extinction_risk"]
        species_image   = request.files["species_image"]
        if species_image:
            species_image.save(f"static/images/species_database/{eng_name}.jpg")
        print(category, extinction_risk)
        add_species(eng_name, latin_name, main_text, category, extinction_risk)
        
        return render_template(
            "species_portal/species_portal_success.jinja",
            eng_name = eng_name,
            )
    except Exception as error_information:
        return render_template(
            "species_portal/species_portal_failed.jinja",
            error_information=error_information
            )
        
