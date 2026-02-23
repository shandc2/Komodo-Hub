from flask import render_template, Blueprint
import sqlite3
import configparser

config = configparser.ConfigParser()

page = Blueprint("species", __name__)

@page.route("/species")
def all_species():
    config.read('config.ini')
    species1 = config['homepage']['featured_species_1']
    species2 = config['homepage']['featured_species_2']
    species3 = config['homepage']['featured_species_3']
    conn = sqlite3.connect("database/species.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # allows dict-style access
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM species")
    species_list = cursor.fetchall()
    
    for sp in species_list:
        print(sp['species_english'])

    conn.close()

    return render_template(
        "species/species.jinja",
        species=species_list,
        species1=species1,
        species2=species2,
        species3=species3,
        )