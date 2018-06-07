# -*- coding: utf-8 -*-

import os

from bio2bel.utils import get_connection, get_data_dir

MODULE_NAME = 'hmdb'
DATA_DIR = get_data_dir(MODULE_NAME)
DEFAULT_CACHE_CONNECTION = get_connection(MODULE_NAME)

#: Data source
DATA_URL = 'http://www.hmdb.ca/system/downloads/current/hmdb_metabolites.zip'
DATA_PATH = os.path.join(DATA_DIR, 'hmdb_metabolites.zip')
DATA_FILE_UNZIPPED = os.path.join(DATA_DIR, 'hmdb_metabolites.xml')

SWEAT_URL = 'http://www.hmdb.ca/system/downloads/current/sweat_metabolites.zip'
SWEAT_FILE = 'sweat_metabolites.xml'

DOID = 'disease-ontology'
HP = 'hp'
MESHD = 'mesh-diseases'

#: Artifactory names of ontologies
ONTOLOGIES = [
    DOID,
    HP,
    MESHD
]

ONTOLOGY_NAMESPACES = {
    DOID: 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/disease-ontology/disease-ontology-20170725.belns',
    HP: 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/hp/hp-20171108.belns',
    MESHD: 'https://arty.scai.fraunhofer.de/artifactory/bel/namespace/mesh-diseases/mesh-diseases-20170725.belns'
}
