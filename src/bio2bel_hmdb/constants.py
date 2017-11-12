# -*- coding: utf-8 -*-

import os

MODULE_NAME = 'hmdb'
BIO2BEL_DIR = os.environ.get('BIO2BEL_DIRECTORY', os.path.join(os.path.expanduser('~'), '.pybel', 'bio2bel'))
DATA_DIR = os.path.join(BIO2BEL_DIR, MODULE_NAME)
os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_CACHE_NAME = '{}.db'.format(MODULE_NAME)
DEFAULT_CACHE_PATH = os.path.join(DATA_DIR, DEFAULT_CACHE_NAME)
DEFAULT_CACHE_CONNECTION = os.environ.get('BIO2BEL_CONNECTION', 'sqlite:///' + DEFAULT_CACHE_PATH)

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
