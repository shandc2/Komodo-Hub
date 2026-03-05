import configparser

from database.db_commands import get_species_by_name

def featured_species_function(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    featured_species_list = list(dict(config["featured_species"]).values())
    featured_species = []
    for species in featured_species_list:
        featured_species.append(get_species_by_name(species))
    
    return featured_species

