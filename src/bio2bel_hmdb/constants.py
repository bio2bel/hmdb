# -*- coding: utf-8 -*-

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'hmdb'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)

#: Data source
DATA_URL = 'http://www.hmdb.ca/system/downloads/current/hmdb_metabolites.zip'
DATA_FILE = 'hmdb_metabolites.xml'

SWEAT_URL = 'http://www.hmdb.ca/system/downloads/current/sweat_metabolites.zip'
SWEAT_FILE = 'sweat_metabolites.xml'

CONFIG_FILE_PATH = os.path.join(DATA_DIR, 'config.ini')

ONTOLOGIES = ['disease-ontology', 'human-phenotype-ontology', 'mesh-diseases']
DISEASE_ONTOLOGY = 'DOID'
HUMAN_PHENOTYPE_ONTOLOGY = 'HPO'
MESH_DISEASES = 'MeSH'
