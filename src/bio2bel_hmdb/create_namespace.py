# -*- coding: utf-8 -*-

from bio2bel_hmdb.constants import HMDB_SQLITE_PATH
from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite, Diseases
from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL, NAMESPACE_DOMAIN_OTHER
from pybel_tools.definition_utils import write_namespace
from pybel_tools.resources import get_latest_arty_namespace
from pybel.utils import get_bel_resource

import logging


def get_hmdb_accession(connection=None):
    """
    Create a list of all HMDB metabolite identifiers present in the database.

    :param str connection: connection string for the manager
    :rtype: list
    """
    if connection == None:
        connection = HMDB_SQLITE_PATH

    manager = Manager(connection)
    accessions = manager.session.query(Metabolite.accession).all()
    if not accessions:
        logging.warning("Database not populated. Please populate database before calling this function")

    return [a[0] for a in accessions]  # if anybody knows a better way of querying for a flat list. Please change.


def get_hmdb_diseases(connection=None):
    """
    Create a list of all disease names present in the database.

    :param str connection: connection string for the manager
    :rtype: list
    """
    if connection == None:
        connection = HMDB_SQLITE_PATH

    manager = Manager(connection)
    accessions = manager.session.query(Diseases.name).all()
    if not accessions:
        logging.warning("Database not populated. Please populate database before calling this function")

    return [a[0] for a in accessions]  # if anybody knows a better way of querying for a flat list. Please change.


def write_hmdb_id_ns(file=None, values=None):
    """
    Create a BEL namespace with HMDB identifiers.

    :param file: file to which the namespace should be written. If None it will be outputted in stdout
    :param values: Values that should be part of the namespace. (HMDB identifiers)
    """
    if values is None:
        values = get_hmdb_accession()

    write_namespace(
        namespace_name='Human Metabolome Database',
        namespace_keyword='HMDB',
        namespace_domain=NAMESPACE_DOMAIN_CHEMICAL,
        author_name='Colin Birkenbihl, Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        author_copyright='Creative Commons by 4.0',
        citation_name='HMDB',
        values=values,
        functions='A',
        file=file
    )


def write_hmdb_disease_ns(file=None, values=None):
    """
    Create a BEL namespace with HMDB disease names.

    :param file: file to which the namespace should be written. If None it will be outputted in stdout
    :param values: Values that should be part of the namespace. (disease names)
    """
    if values is None:
        values = get_hmdb_diseases()

    write_namespace(
        namespace_name='Human Metabolome Database Disease Names',
        namespace_keyword='HMDB_D',
        namespace_domain=NAMESPACE_DOMAIN_OTHER,
        author_name='Colin Birkenbihl, Charles Tapley Hoyt',
        author_contact='charles.hoyt@scai.fraunhofer.de',
        author_copyright='Creative Commons by 4.0',
        citation_name='HMDB_D',
        values=values,
        functions='O',
        file=file
    )

def construct_hmdb_disease_mapping():
    """
    constructs a mapping of hmdb disease names to actually useful ontologies.

    :return:
    """
    def check_disease_doid(hmdb_disease):

        doid_path = get_latest_arty_namespace('disease-ontology')
        doid_ns = get_bel_resource()

        doid_values = doid_ns['values']


