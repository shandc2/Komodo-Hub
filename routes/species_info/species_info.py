from flask import render_template, Blueprint
import sqlite3

species_info_page = Blueprint("species_information", __name__)


def animal_from_database(species_id):
    conn = sqlite3.connect("database/species.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT species_id,
               species_english,
               species_latin,
               body_text,
               created_at
        FROM species
        WHERE species_english = ?
    """,
        (species_id,),
    )

    row = cursor.fetchone()
    conn.close()
    print(row)
    return row


# animal_from_database expects five variables:
# id, english_name, latin_name, body_text and created_at
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


@species_info_page.route("/species/<species_id>")
def data(species_id):
    var1, var2, latin_name, body_text, var5 = animal_from_database(species_id)
    return render_template(
        "species_information/species_information.jinja",
        english_name=var2,
        latin_name=latin_name,
        main_text=body_text,
    )
