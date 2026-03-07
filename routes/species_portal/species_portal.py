from flask import render_template, Blueprint, request, redirect, url_for
from database.db_commands import add_species, delete_species, get_species_by_name, get_species_by_id
import os
import uuid

page = Blueprint("species_portal", __name__, url_prefix="/species/portal")


@page.route("/")
def portal():
    return render_template("species_portal/species_portal.jinja")


@page.route("/", methods=["POST"])
def add_species_to_database():
    try:
        eng_name        = request.form["eng_name"].title()
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
    except ValueError as error_information:
        species_to_edit = get_species_by_name(request.form["eng_name"].title())
        species_id = species_to_edit['species_id']
        return redirect(url_for("species_editor.edit_species", species_id=species_id))
    except Exception as error_information:
        return render_template(
            "species_portal/species_portal_failed.jinja",
            error_information=error_information
            )
        
@page.route("/<eng_name>")
def portal_success(eng_name):
    return render_template(
            "species_portal/species_portal_success.jinja",
            eng_name = eng_name,
            )