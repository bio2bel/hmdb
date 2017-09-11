# -*- coding: utf-8 -*-

"""
Work in progress
- import database model
- change get_data() to work with xml parser
- write populate function
"""

import configparser
import logging
import os

import requests
import zipfile
from io import BytesIO

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base #import database tables
from .constants import (
    DATA_URL,
    HMDB_SQLITE_PATH,
    HMDB_CONFIG_FILE_PATH,
)

log = logging.getLogger(__name__)


def get_data(source=None):
    """Download HMDB data"""

    req = requests.get(DATA_URL)
    hmdb_zip = zipfile.ZipFile(BytesIO(req.content))
    hmdb_text = hmdb_zip.open("hmdb_metabolites.xml").read()
    hmdb_text = hmdb_text.decode('UTF-8')

    return hmdb_text


class Manager(object):
    def __init__(self, connection=None):
        self.connection = self.get_connection(connection)
        self.engine = create_engine(self.connection)
        self.sessionmake = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        self.session = self.sessionmake()
        self.make_tables()

    @staticmethod
    def get_connection(connection=None):
        """Return the SQLAlchemy connection string if it is set

        :param connection: get the SQLAlchemy connection string
        :rtype: str
        """

        if connection:
            return connection

        config = configparser.ConfigParser()

        cfp = HMDB_CONFIG_FILE_PATH

        if os.path.exists(cfp):
            log.info('fetch database configuration from {}'.format(cfp))
            config.read(cfp)
            connection = config['database']['sqlalchemy_connection_string']
            log.info('load connection string from {}: {}'.format(cfp, connection))
            return connection

        with open(cfp, 'w') as config_file:
            config['database'] = {'sqlalchemy_connection_string': HMDB_SQLITE_PATH}
            config.write(config_file)
            log.info('create configuration file {}'.format(cfp))

        return HMDB_SQLITE_PATH

    def make_tables(self, check_first=True):
        """Create tables from model.py"""
        Base.metadata.create_all(self.engine, checkfirst=check_first)

    def populate(self, source=None):
        """Populate database with HMDB data"""

        if not source:
            text = get_data()
        else:
            pass

        raise NotImplementedError




