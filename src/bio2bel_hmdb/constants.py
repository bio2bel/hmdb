# -*- coding: utf-8 -*-

import os

#: Data source
DATA_URL = 'http://www.hmdb.ca/system/downloads/current/hmdb_metabolites.zip'
DATA_FILE = 'hmdb_metabolites.xml'

SWEAT_URL = 'http://www.hmdb.ca/system/downloads/current/sweat_metabolites.zip'
SWEAT_FILE = 'sweat_metabolites.xml'

HMDB_DATA_DIR = os.path.join(os.path.expanduser('~'), '.pyhmdb')

if not os.path.exists(HMDB_DATA_DIR):
    os.makedirs(HMDB_DATA_DIR)

HMDB_DATABASE_NAME = 'hmdb.db'
HMDB_SQLITE_PATH = 'sqlite:///' + os.path.join(HMDB_DATA_DIR, HMDB_DATABASE_NAME)

HMDB_CONFIG_FILE_PATH = os.path.join(HMDB_DATA_DIR, 'config.ini')

ONTOLOGIES = ['disease-ontology', 'human-phenotype-ontology', 'mesh-diseases']
DISEASE_ONTOLOGY = 'DION'
HUMAN_PHENOTYPE_ONTOLOGY = 'HPO'
MESH_DISEASES = 'MESH'
