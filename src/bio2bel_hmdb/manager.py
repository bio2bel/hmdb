# -*- coding: utf-8 -*-

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
from .models import Base, Metabolite, Biofluids, MetaboliteBiofluid, \
    Synonyms, SecondaryAccessions, Tissues, MetaboliteTissues, \
    Pathways, MetabolitePathways, Proteins, MetaboliteProteins, References, MetaboliteReferences

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

    def get_tag(self, element_tag):
        """Function to delete the xml namespace prefix when calling element.tag

        :param element_tag: tag attribute of an xml element
        :rtype: str
        """
        return element_tag.split("}")[1]

    def populate_with_1_layer_elements(self, element, metabolite_instance, instance_dict, table, relation_table):
        """

        :param element: the current parent XML element. E.g. "pathways" where the children would have the tag "pathway" .
        :param models.Metabolite metabolite_instance: metabolite object which is associated with the instances (e.g. is
        involved in that "pathway")
        :param dict instance_dict: dictionary which tracks if the found instance is already present in the table and can
        then refer to it
        :param class table: sqlalchemy class to which the instances belong. E.g. "Pathways"
        :param class relation_table: sqlalchemy class which stores the many to many relation between the instances and
        the metabolites
        :param str instance_dict_key: String which is used as the key for the instance_dict. (to ensure uniqueness in
        the instance_dict)
        :rtype: dict
        """
        for instance_element in element:
            instance_dict_key = instance_element.text

            if instance_dict_key not in instance_dict:  # check if biofluid is already in table
                instance_dict[instance_dict_key] = table(biofluid=instance_dict_key)
                self.session.add(instance_dict[instance_dict_key])

            # create metabolite-biofluid relation object
            new_meta_rel = relation_table(metabolite=metabolite_instance, biofluid=instance_dict[instance_dict_key])
            self.session.add(new_meta_rel)
        return instance_dict

    def populate_with_2_layer_elements(self, element, metabolite_instance, instance_dict, table, relation_table,
                                       instance_dict_key=None):
        """Function to parse two layered xml elements (parent elements covers at least one child
        which also consists of one more layer of tags) and populate sqlalchemy tables.

        :param element: the current parent XML element. E.g. "pathways" where the children would have the tag "pathway".
        :param models.Metabolite metabolite_instance: metabolite object which is associated with the instances (e.g. is
        involved in that "pathway")
        :param dict instance_dict: dictionary which tracks if the found instance is already present in the table and can
        then refer to it
        :param class table: sqlalchemy class to which the instances belong. E.g. "Pathways"
        :param class relation_table: sqlalchemy class which stores the many to many relation between the instances and
        the metabolites
        :param str instance_dict_key: String which is used as the key for the instance_dict. (to ensure uniqueness in
        the instance_dict)
        :rtype: dict
        """
        if instance_dict_key is None and len(element) > 0:
            instance_dict_key = self.get_tag(element[0][0].tag)

        for instance_element in element:
            # build pathway object dict to create pathway object
            instance_object_dict = {}

            # create pathway instance
            for instance_sub_element in instance_element:
                cutted_pathway_tag = self.get_tag(instance_sub_element.tag)
                instance_object_dict[cutted_pathway_tag] = instance_sub_element.text

            # add MetabolitePathway relation and continue with next pathway if pathway already present in Pathways
            if instance_object_dict[instance_dict_key] in instance_dict:
                new_meta_rel = relation_table(metabolite=metabolite_instance,
                                              pathway=instance_dict[instance_object_dict[instance_dict_key]])
                self.session.add(new_meta_rel)
                continue

            instance_dict[instance_object_dict[instance_dict_key]] = table(**instance_object_dict)
            self.session.add(instance_dict[instance_object_dict[instance_dict_key]])

            new_meta_rel = relation_table(metabolite=metabolite_instance,
                                          pathway=instance_dict[instance_object_dict[instance_dict_key]])
            self.session.add(new_meta_rel)
        return instance_dict

    def populate(self, source=None):
        """Populate database with HMDB data"""

        # construct xml tree
        tree = get_data(source)
        root = tree.getroot()

        # dicts to check unique constraints for specific tables
        biofluids_dict = {}
        tissues_dict = {}
        pathways_dict = {}
        proteins_dict = {}
        references_dict = {}

        for metabolite in root:
            # create metabolite dict used to feed in main metabolite table
            metabolite_instance = Metabolite()

            for element in metabolite:
                # delete namespace prefix
                tag = self.get_tag(element.tag)

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
                    biofluids_dict = self.populate_with_1_layer_elements(element, metabolite_instance, biofluids_dict,
                                                                         Biofluids, MetaboliteBiofluid)

                elif tag == "tissue_locations":
                    for tissue_element in element:
                        tissue = tissue_element.text
                        if tissue not in tissues_dict:  # check if tissue is already in table
                            tissues_dict[tissue] = Tissues(tissue=tissue)
                            self.session.add(tissues_dict[tissue])

                        new_meta_tissue = MetaboliteTissues(metabolite=metabolite_instance, tissue=tissues_dict[tissue])
                        self.session.add(new_meta_tissue)

                elif tag == "pathways":
                    pathways_dict = self.populate_with_2_layer_elements(element, metabolite_instance, pathways_dict,
                                                                        Pathways, MetabolitePathways)

                elif tag == "normal_concentrations":
                    continue
                elif tag == "abnormal_concentrations":
                    continue
                elif tag == "diseases":
                    continue

                elif tag == "general_references":
                    continue
                    references_dict = self.populate_with_2_layer_elements(element, metabolite_instance, references_dict,
                                                                          References, MetaboliteReferences, "pubmed_id")

                elif tag == "protein_associations":
                    continue
                    proteins_dict = self.populate_with_2_layer_elements(element, metabolite_instance, proteins_dict,
                                                                        Proteins, MetaboliteProteins)

                else:  # feed in main metabolite table
                    setattr(metabolite_instance, tag, element.text)

            self.session.add(metabolite_instance)

        self.session.commit()
