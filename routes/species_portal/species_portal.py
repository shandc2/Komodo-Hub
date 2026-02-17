from flask import render_template, Blueprint

species_portal = Blueprint('species_portal', __name__, url_prefix='/species_portal')

@species_portal.route('/')
def portal():
    return render_template('species_portal/species_portal.jinja')