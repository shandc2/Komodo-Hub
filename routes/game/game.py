from flask import render_template, Blueprint
from database.db_commands import get_all_species

page = Blueprint('game', __name__)


@page.route('/game')
def game():
    species = get_all_species()
    species_list = [s['species_english'] for s in species]
    return render_template('game/game.jinja', species_list=species_list)