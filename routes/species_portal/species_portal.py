from flask import render_template, Blueprint, request

page = Blueprint("species_portal", __name__, url_prefix="/species_portal")


@page.route("/")
def portal():
    return render_template("species_portal/species_portal.jinja")


@page.route("/", methods=["POST"])
def add_species_to_database():
    try:
        eng_name = request.form["eng_name"]
        latin_name = request.form["latin_name"]
        main_text = request.form["main_text"]
        species_image = request.files["species_image"]
        return render_template(
            "species_portal/species_portal_success.jinja",
            eng_name = eng_name,
            )
    except:
        return render_template("species_portal/species_portal_failed.jinja")
    # return f"{eng_name}, {latin_name}, {main_text}"
