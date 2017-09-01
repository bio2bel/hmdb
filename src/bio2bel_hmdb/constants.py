# -*- coding: utf-8 -*-

import os

#: Data source
DATA_URL = 'http://www.hmdb.ca/system/downloads/current/hmdb_metabolites.zip'

HMDB_DATA_DIR = os.path.join(os.path.expanduser('~'), '.pyhmdb')

if not os.path.exists(HMDB_DATA_DIR):
    os.makedirs(HMDB_DATA_DIR)

HMDB_DATABASE_NAME = 'hmdb.db'
HMDB_SQLITE_PATH = 'sqlite:///' + os.path.join(HMDB_DATA_DIR, HMDB_DATABASE_NAME)

HMDB_CONFIG_FILE_PATH = os.path.join(HMDB_DATA_DIR, 'config.ini')
