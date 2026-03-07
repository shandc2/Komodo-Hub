from flask import render_template, Blueprint, request, redirect, url_for
from database.db_commands import delete_species, get_species_by_id, update_species
import uuid

page = Blueprint("species_editor", __name__, url_prefix="/species/editor")


@page.route("/<species_id>")
def edit_species(species_id):
    species_to_edit = get_species_by_id(species_id)
    print(species_id)
    return render_template(
        'species_portal/species_editor.jinja',
        sp = species_to_edit,
        species_id = species_id
        )

@page.route("/<species_id>", methods=["POST"])
def species_update(species_id):
    try:
        eng_name        = request.form["eng_name"].title()
        latin_name      = request.form["latin_name"].capitalize()
        main_text       = request.form["main_text"]
        category        = request.form["category"].capitalize()
        extinction_risk = request.form["extinction_risk"]
        species_image   = request.files.get("species_image")

        image_id = ""

        if species_image and species_image.filename:
            image_id = str(uuid.uuid4())
            species_image.save(f"static/images/species_database/{image_id}.jpg")

        update_species(species_id, eng_name, latin_name, main_text, category, extinction_risk)

        return redirect(url_for("species_information.data", species_english=eng_name))

    except Exception as error_information:
        return render_template(
            "species_portal/species_portal_failed.jinja",
            error_information=error_information
        )
        
@page.route("/<eng_name>")
def edit_success(eng_name):
    return render_template(
            "species_portal/species_portal_success.jinja",
            eng_name = eng_name,
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