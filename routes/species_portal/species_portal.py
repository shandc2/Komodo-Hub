from flask import render_template, Blueprint, request, redirect, url_for
from database.db_commands import add_species, delete_species, get_species_by_name
import os
import uuid

page = Blueprint("species_portal", __name__, url_prefix="/species/portal")


@page.route("/")
def portal():
    return render_template("species_portal/species_portal.jinja")


@page.route("/", methods=["POST"])
def add_species_to_database():
    try:
        eng_name        = request.form["eng_name"].capitalize()
        latin_name      = request.form["latin_name"].capitalize()
        main_text       = request.form["main_text"]
        category        = request.form["category"].capitalize()
        extinction_risk = request.form["extinction_risk"]
        species_image   = request.files["species_image"]
        image_id        = ""
        if species_image:
            image_id = str(uuid.uuid4())
            species_image.save(f"static/images/species_database/{image_id}.jpg")
        print(category, extinction_risk)
        add_species(eng_name, latin_name, main_text, category, extinction_risk, image_id)
        
        return render_template(
            "species_portal/species_portal_success.jinja",
            eng_name = eng_name,
            )
    except Exception as error_information:
        return render_template(
            "species_portal/species_portal_failed.jinja",
            error_information=error_information
            )


@page.route("/delete/<species_english>", methods=["POST"])
def delete_species_from_database(species_english):
    try:
        entry = get_species_by_name(species_english)
        if entry is None:
            raise ValueError(f"Species '{species_english}' not found.")
        delete_species(entry["species_id"])
        return redirect(url_for("species.all_species"))
    except Exception as error_information:
        return render_template(
            "species_portal/species_portal_failed.jinja",
            error_information=error_information
        )