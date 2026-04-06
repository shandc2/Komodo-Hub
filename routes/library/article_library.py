from flask import render_template, Blueprint, request
import configparser

from database.db_commands import get_all_articles, search_species, get_species_by_name
from utilities.featured_species import featured_species_function

config = configparser.ConfigParser()

page = Blueprint("articles", __name__, url_prefix="/articles")

# article library page
@page.route("")
def all_species():
    article_list = get_all_articles()
        
    article_list = sorted(article_list, key=lambda sp: sp["title"])
    
    for sp in article_list:
        print(sp['title'])

    return render_template("library/library.jinja", articles=article_list)
    
# search page
@page.route("/search")
def search():
    query = request.args.get("search-query")

    results = search_species(query)
    print(results)
    return render_template("/species/species_search.jinja", results=results, query=query)