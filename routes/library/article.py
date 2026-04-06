from flask import render_template, Blueprint, send_from_directory
from database.db_commands import get_article_by_id, get_species_by_id
import sqlite3

page = Blueprint("article", __name__)

# this page works by taking the species name (in english) from the url and using that to read the database.
# Because of this we are able to create one page and simply generate links based on the contents of the database
# i.e. we can create a button with the hyperlink /species/iguana and this will
# allow the user to view the information about the species
# please be aware the page expects a .jpg at:
# /static/images/species_database/{{photoid}}.jpg but this will be generated automatically
# so long as you use the species_portal or species editor pages I created - CS


@page.route("/articles/<article_id>")
def data(article_id):
    database_entry = get_article_by_id(article_id)
    if database_entry is None:
        raise TypeError(f"No article named '{article_id}' found in the database.")
    return render_template(
        "library/article.jinja",
        article_id  =database_entry["article_id"   ].capitalize(),
        title       =database_entry["title"     ].capitalize(),
        subtitle    =database_entry["subtitle"         ],
        main_text   =database_entry["main_text"          ].capitalize(),
        author      =database_entry["author"   ],
        publish_date=database_entry["publish_date"           ])

@page.route("/species/image/<photoid>")
def image(photoid):
    return send_from_directory("database/images", photoid)