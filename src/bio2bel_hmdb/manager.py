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
from sqlalchemy.exc import IntegrityError

from .constants import (
    DATA_URL,
    HMDB_SQLITE_PATH,
    HMDB_CONFIG_FILE_PATH,
)
from .models import Base, Metabolite, Biofluids, MetaboliteBiofluid, \
    Synonyms, SecondaryAccessions, Tissues, MetaboliteTissues, \
    Pathways, MetabolitePathways

log = logging.getLogger(__name__)


def get_data(source=None):
    """Download HMDB data"""

    if not source:
        req = requests.get(DATA_URL)
        hmdb_zip = zipfile.ZipFile(BytesIO(req.content))
        hmdb_zip.extract("hmdb_metabolites.xml")
        source = "hmdb_metabolites.xml"
        tree = ET.parse(source)
        # clean up
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

        :param connection: SQLAlchemy connection string
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
            """Function to delete the xml namespace prefix when calling element.tag

            :param element_tag: tag attribute of an xml element
            :rtype: str
            """
            return element_tag.split("}")[1]

        # construct xml tree
        tree = get_data(source)
        root = tree.getroot()

        # dicts to check unique constraints for specific tables
        biofluids_dict = {}
        tissues_dict = {}
        pathways_dict = {}

        for metabolite in root:
            # create metabolite dict used to feed in main metabolite table
            metabolite_instance = Metabolite()

            for element in metabolite:
                # delete namespace prefix
                tag = get_tag(element.tag)

                # handle wikipedia typo in xml tags
                if tag == "wikipidia":
                    tag = "wikipedia"
                elif tag == "wikipedia":
                    log.warning("HMDB fixed the 'wikipidia' tag to 'wikipedia'. Change code.")

                # handle seperate tables and nested iterations (Work In Progress)
                if tag == "secondary_accessions":
                    for secondary_accession_element in element:
                        new_secondary_accession = SecondaryAccessions(metabolite=metabolite_instance,
                                                                      secondary_accession=secondary_accession_element.text)
                        self.session.add(new_secondary_accession)

                elif tag == "synonyms":
                    for synonym_element in element:
                        new_synonym = Synonyms(metabolite=metabolite_instance, synonym=synonym_element.text)
                        self.session.add(new_synonym)

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
                    for biofluid_element in element:
                        biofluid = biofluid_element.text
                        if biofluid not in biofluids_dict:  # check if biofluid is already in table
                            biofluids_dict[biofluid] = Biofluids(biofluid=biofluid)
                            self.session.add(biofluids_dict[biofluid])

                        # create metabolite-biofluid relation object
                        new_meta_bio = MetaboliteBiofluid(metabolite=metabolite_instance,
                                                          biofluid=biofluids_dict[biofluid])
                        self.session.add(new_meta_bio)

                elif tag == "tissue_locations":
                    for tissue_element in element:
                        tissue = tissue_element.text
                        if tissue not in tissues_dict:  # check if tissue is already in table
                            tissues_dict[tissue] = Tissues(tissue=tissue)
                            self.session.add(tissues_dict[tissue])

                        new_meta_tissue = MetaboliteTissues(metabolite=metabolite_instance,
                                                            tissue=tissues_dict[tissue])
                        self.session.add(new_meta_tissue)

                elif tag == "pathways":
                    if len(element.getchildren()) < 1:
                        continue

                    for pathway_element in element:

                        # build pathway object dict to create pathway object
                        pathway_object_dict = {}
                        for pathway_sub_element in pathway_element:
                            cutted_pathway_tag = get_tag(pathway_sub_element.tag)
                            pathway_object_dict[cutted_pathway_tag] = pathway_sub_element.text

                        # break if pathway already present in table
                        if pathway_object_dict['name'] in pathways_dict:
                            continue

                        pathways_dict[pathway_object_dict['name']] = Pathways(**pathway_object_dict)
                        self.session.add(pathways_dict[pathway_object_dict['name']])

                    new_meta_path = MetabolitePathways(metabolite=metabolite_instance,
                                                       pathway=pathways_dict[pathway_object_dict['name']])
                    self.session.add(new_meta_path)

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
                else:  # feed in main metabolite table
                    setattr(metabolite_instance, tag, element.text)

            self.session.add(metabolite_instance)

        self.session.commit()
