from flask import render_template, Blueprint

page = Blueprint('species_portal', __name__, url_prefix='/species_portal')

@page.route('/')
def portal():
    return render_template('species_portal/species_portal.jinja')