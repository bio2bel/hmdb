# -*- coding: utf-8 -*-

"""
Work in progress
- import database models
- write populate function
"""

import configparser
import logging
import zipfile
import xml.etree.ElementTree as ET

import os
import requests
from io import BytesIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .constants import (
    DATA_URL,
    HMDB_SQLITE_PATH,
    HMDB_CONFIG_FILE_PATH,
)
from .models import Base, Metabolite, Biofluids, MetaboliteBiofluid  # import database tables

log = logging.getLogger(__name__)


def get_data(source=None):
    """Download HMDB data"""

    if not source:
        req = requests.get(DATA_URL)
        hmdb_zip = zipfile.ZipFile(BytesIO(req.content))
        hmdb_zip.extract("hmdb_metabolites.xml")
        source = "hmdb_metabolites.xml"
        tree = ET.parse(source)
        #clean up
        os.remove(source)
    else:
        tree = ET.parse(source)

    return tree


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

        def get_tag(element_tag):
            """Function to delete the xml namespace prefix when calling element.tag"""
            return element_tag.split("}")[1]

        #construct xml tree
        tree = get_data(source)
        root = tree.getroot()

        for metabolite in root:
            #create metabolite dict used to feed in main metabolite table
            metabolite_dict = {}

            for element in metabolite:
                #delete namespace prefix
                tag = get_tag(element.tag)
                #handle wikipedia typo in xml tags
                if tag == "wikipidia":
                    tag = "wikipedia"

                #handle seperate tables and nested iterations (Work In Progress)
                if tag == "secondary_accessions":
                    continue
                elif tag == "synonyms":
                    continue
                elif tag == "taxonomy":
                    continue
                elif tag == "ontology":
                    continue
                elif tag == "experimental_properties":
                    continue
                elif tag == "predicted_properties":
                    continue
                elif tag == "spectra":
                    continue
                elif tag == "biofluid_locations":
                    continue
                elif tag == "tissue_locations":
                    continue
                elif tag == "pathways":
                    continue
                elif tag == "normal_concentrations":
                    continue
                elif tag == "abnormal_concentrations":
                    continue
                elif tag == "diseases":
                    continue
                elif tag == "general_references":
                    continue
                elif tag == "protein_associations":
                    continue
                else: #feed in main metabolite table
                    metabolite_dict[tag] = element.text

            new_metabolite = Metabolite(**metabolite_dict)
            self.session.add(new_metabolite)

        self.session.commit()
