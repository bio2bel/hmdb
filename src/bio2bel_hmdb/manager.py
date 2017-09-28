# -*- coding: utf-8 -*-

import configparser
import logging
import xml.etree.ElementTree as ET
import zipfile

import os
import requests
from io import BytesIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bio2bel_hmdb.constants import (
    DATA_URL,
    HMDB_SQLITE_PATH,
    HMDB_CONFIG_FILE_PATH,
)
from bio2bel_hmdb.models import Base, Metabolite, Biofluids, MetaboliteBiofluid, \
    Synonyms, SecondaryAccessions, Tissues, MetaboliteTissues, \
    Pathways, MetabolitePathways, Proteins, MetaboliteProteins, References, MetaboliteReferences, Diseases, \
    MetaboliteDiseasesReferences, Biofunctions, MetaboliteBiofunctions, CellularLocations, MetaboliteCellularLocations

log = logging.getLogger(__name__)


def get_data(source=None):
    """Download HMDB data

    :param str source: String representing the filename of a .xml file which should be taken as input for the database
    construction. If None the full HMDB metabolite .xml will be downloaded and used to populate the database.
    """

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
    """
    The manager is handling the database construction, population and querying.
    """

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

    @staticmethod
    def ensure(connection=None):
        """Checks and allows for a Manager to be passed to the function.

        :param connection: can be either a already build manager or a connection string to build a manager with.
        """
        if connection is None or isinstance(connection, str):
            return Manager(connection=connection)

        if isinstance(connection, Manager):
            return connection

        raise TypeError

    def make_tables(self, check_first=True):
        """Create tables from model.py"""
        Base.metadata.create_all(self.engine, checkfirst=check_first)

    def get_tag(self, element_tag):
        """Function to delete the xml namespace prefix when calling element.tag

        :param element_tag: tag attribute of an xml element
        :rtype: str
        """
        return element_tag.split("}")[1]

    def _populate_with_1_layer_elements(self, element, metabolite_instance, instance_dict, table, relation_table,
                                        column_name):
        """

        :param element: the current parent XML element. E.g. "pathways" where the children would have the tag "pathway".
        :param models.Metabolite metabolite_instance: metabolite object which is associated with the instances (e.g. is
        involved in that "pathway")
        :param dict instance_dict: dictionary which tracks if the found instance is already present in the table and can
        then refer to it
        :param class table: sqlalchemy class to which the instances belong. E.g. "Pathways"
        :param class relation_table: sqlalchemy class which stores the many to many relation between the instances and
        the metabolites
        :param str column_name: Name of the column in the relation tables which does not represent the metabolite.
        e.g. reference, pathway etc
        :rtype: dict
        """
        for instance_element in element:
            instance_dict_key = instance_element.text

            if instance_dict_key not in instance_dict:  # check if biofluid is already in table
                new_instance_dict = {column_name: instance_dict_key}
                instance_dict[instance_dict_key] = table(**new_instance_dict)
                self.session.add(instance_dict[instance_dict_key])

            # create metabolite-biofluid relation object
            new_meta_rel_dict = {"metabolite": metabolite_instance, column_name: instance_dict[instance_dict_key]}
            new_meta_rel = relation_table(**new_meta_rel_dict)
            self.session.add(new_meta_rel)
        return instance_dict

    def _populate_with_2_layer_elements(self, element, metabolite_instance, instance_dict, table, relation_table,
                                        column,
                                        instance_dict_key=None, metabolite_column='metabolite'):
        """Function to parse two layered xml elements (parent elements covers at least one child
        which also consists of one more layer of tags) and populate sqlalchemy tables.

        :param element: the current parent XML element. E.g. "pathways" where the children would have the tag "pathway".
        :param models.Metabolite metabolite_instance: metabolite object which is associated with the instances (e.g. is
        involved in that "pathway")
        :param dict instance_dict: dictionary which tracks if the found instance is already present in the table and can
        then refer to it
        :param type table: sqlalchemy class to which the instances belong. E.g. "Pathways"
        :param type relation_table: sqlalchemy class which stores the many to many relation between the instances and
        the metabolites
        :param str column: column name of the relation table which is not the metabolite
        :param str instance_dict_key: String which is used as the key for the instance_dict. (to ensure uniqueness in
        the instance_dict)
        :param str metabolite_column: column of the relation table which represents the foreignkey to the main table.
        In our database model the Metabolite table.
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
                new_meta_rel_dict = {
                    metabolite_column: metabolite_instance,
                    column: instance_dict[instance_object_dict[instance_dict_key]]
                }
                new_meta_rel = relation_table(**new_meta_rel_dict)
                self.session.add(new_meta_rel)
                continue

            instance_dict[instance_object_dict[instance_dict_key]] = table(**instance_object_dict)
            self.session.add(instance_dict[instance_object_dict[instance_dict_key]])

            new_meta_rel_dict = {
                metabolite_column: metabolite_instance,
                column: instance_dict[instance_object_dict[instance_dict_key]]
            }
            new_meta_rel = relation_table(**new_meta_rel_dict)
            self.session.add(new_meta_rel)

        return instance_dict

    def _handle_diseases(self, element, references_dict, diseases_dict, metabolite_instance):
        """
        This function has the purpose of keeping the populate function smaller
        and to populate the database with disease and related reference information.

        :param element: Element object from the xml ElementTree
        :param references_dict: Dictionary to keep track of which references are already in the database
        :param diseases_dict: Dictionary to keep track of which diseases are already in the database
        :param metabolite_instance: Metabolite object to which the diseases and references are related
        :return:
        """
        for disease_element in element:
            disease_instance = Diseases()

            for disease_sub_element in disease_element:

                dtag = self.get_tag(disease_sub_element.tag)

                if dtag != "references":
                    setattr(disease_instance, dtag, disease_sub_element.text)
                else:
                    if disease_instance.name not in diseases_dict:  # add disease instance if not already in table
                        diseases_dict[disease_instance.name] = disease_instance
                        self.session.add(disease_instance)

                    for reference_element in disease_sub_element:
                        new_reference_object_dict = {}  # dict to check if reference is already presend in table

                        for reference_sub_element in reference_element:  # construct new reference object
                            reference_tag = self.get_tag(reference_sub_element.tag)
                            new_reference_object_dict[reference_tag] = reference_sub_element.text

                        # add if not already in reference table
                        if new_reference_object_dict['pubmed_id'] not in references_dict:
                            references_dict[new_reference_object_dict['pubmed_id']] = References(
                                **new_reference_object_dict)
                            self.session.add(references_dict[new_reference_object_dict['pubmed_id']])

                        rel_meta_dis_ref = MetaboliteDiseasesReferences(metabolite=metabolite_instance,
                                                                        disease=diseases_dict[
                                                                            disease_instance.name],
                                                                        reference=references_dict[
                                                                            new_reference_object_dict[
                                                                                'pubmed_id']])
                        self.session.add(rel_meta_dis_ref)
        return references_dict, diseases_dict

    def populate(self, source=None):
        """
        Populate database with the HMDB data.

        :param str source:
        """

        # construct xml tree
        tree = get_data(source)
        root = tree.getroot()

        # dicts to check unique constraints for specific tables
        biofluids_dict = {}
        tissues_dict = {}
        pathways_dict = {}
        proteins_dict = {}
        references_dict = {}
        diseases_dict = {}
        biofunctions_dict = {}
        cellular_locations_dict = {}

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

                if tag == "secondary_accessions":
                    for secondary_accession_element in element:
                        new_secondary_accession = SecondaryAccessions(metabolite=metabolite_instance,
                                                                      secondary_accession=secondary_accession_element.text)
                        self.session.add(new_secondary_accession)

                elif tag == "synonyms":
                    for synonym_element in element:
                        new_synonym = Synonyms(metabolite=metabolite_instance, synonym=synonym_element.text)
                        self.session.add(new_synonym)

                elif tag == "taxonomy":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "ontology":
                    for ontology_element in element:
                        ontology_tag = self.get_tag(ontology_element.tag)

                        if ontology_tag == "biofunctions":
                            biofunctions_dict = self._populate_with_1_layer_elements(ontology_element,
                                                                                     metabolite_instance,
                                                                                     biofunctions_dict, Biofunctions,
                                                                                     MetaboliteBiofunctions,
                                                                                     "biofunction")
                        if ontology_tag == "cellular_locations":
                            cellular_locations_dict = self._populate_with_1_layer_elements(ontology_element,
                                                                                           metabolite_instance,
                                                                                           cellular_locations_dict,
                                                                                           CellularLocations,
                                                                                           MetaboliteCellularLocations,
                                                                                           "cellular_location")

                elif tag == "experimental_properties":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "predicted_properties":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "spectra":  # will not be processed since the corresponding database is down
                    continue

                elif tag == "biofluid_locations":
                    biofluids_dict = self._populate_with_1_layer_elements(element, metabolite_instance, biofluids_dict,
                                                                          Biofluids, MetaboliteBiofluid, 'biofluid')

                elif tag == "tissue_locations":
                    tissues_dict = self._populate_with_1_layer_elements(element, metabolite_instance, tissues_dict,
                                                                        Tissues, MetaboliteTissues, 'tissue')

                elif tag == "pathways":
                    pathways_dict = self._populate_with_2_layer_elements(element, metabolite_instance, pathways_dict,
                                                                         Pathways, MetabolitePathways, 'pathway')

                elif tag == "normal_concentrations":  # will be delayed to later versions since not important for BEL
                    continue
                elif tag == "abnormal_concentrations":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "diseases":
                    references_dict, diseases_dict = self._handle_diseases(element, references_dict,
                                                                           diseases_dict, metabolite_instance)

                elif tag == "general_references":
                    references_dict = self._populate_with_2_layer_elements(element, metabolite_instance,
                                                                           references_dict,
                                                                           References, MetaboliteReferences,
                                                                           'reference',
                                                                           "pubmed_id")

                elif tag == "protein_associations":
                    proteins_dict = self._populate_with_2_layer_elements(element, metabolite_instance, proteins_dict,
                                                                         Proteins, MetaboliteProteins, 'protein')

                else:  # feed in main metabolite table
                    setattr(metabolite_instance, tag, element.text)

            self.session.add(metabolite_instance)

        self.session.commit()

    def get_metabolite_by_accession(self, hmdb_metabolite_accession):
        """

        :param str hmdb_metabolite_accession: The HMDB acession
        :rtype: Metabolite
        """
        return self.session.query(Metabolite).filter(Metabolite.accession == hmdb_metabolite_accession).one_or_none()

    def query_metabolite_associated_proteins(self, hmdb_metabolite_id):
        """
        Function to query the constructed HMDB database to get the metabolite associated protein relations
        for BEL enrichment

        :param str hmdb_metabolite_id:
        :rtype: list
        """
        metabolite = self.get_metabolite_by_accession(hmdb_metabolite_id)
        return metabolite.proteins

    def query_metabolite_associated_diseases(self, hmdb_metabolite_id):
        """Function to query the constructed HMDB database to get the metabolite associated disease relations
         for BEL enrichment

        :param str hmdb_metabolite_id:
        :rtype: list
        """
        metabolite = self.get_metabolite_by_accession(hmdb_metabolite_id)
        return metabolite.diseases

    def query_disease_associated_metabolites(self, disease_name):
        """
        Query function that returns a list of metabolite-disease interactions, which are associated to a disease.

        :param disease_name:
        :rtype: list
        """
        return self.session.query(Diseases).filter(Diseases.name == disease_name).first().metabolites

    def query_protein_associated_metabolites(self, uniprot_id):
        """
        Query function that returns a list of metabolite-disease interactions, which are associated to a disease.

        :param uniprot_id: uniprot identifier of a protein for which the associated metabolite relations should be outputted
        :rtype: list
        """
        return self.session.query(Proteins).filter(Proteins.uniprot_id == uniprot_id).first().metabolites
