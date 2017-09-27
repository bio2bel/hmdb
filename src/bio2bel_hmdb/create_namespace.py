# -*- coding: utf-8 -*-

from bio2bel_hmdb.constants import HMDB_SQLITE_PATH
from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite, Diseases
from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL, NAMESPACE_DOMAIN_OTHER
from pybel_tools.definition_utils import write_namespace


def get_hmdb_accession():
    """ """
    m = Manager(HMDB_SQLITE_PATH)

    accessions = m.session.query(Metabolite.accession).all()
    return [a[0] for a in accessions]  # if anybody knows a better way of querying for a flat list. Please change.


def get_hmdb_diseases():
    """ """
    m = Manager(HMDB_SQLITE_PATH)

    accessions = m.session.query(Diseases.name).all()
    return [a[0] for a in accessions]  # if anybody knows a better way of querying for a flat list. Please change.


def write_hmdb_belns(file=None, values=None):
    """
    Function to create a BEL namespace with HMDB identifiers.

    :param file: file to which the namespace should be written. If None it will be outputted in stdout
    :param values: Values that should be part of the namespace. here HMDB identifiers
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
    Function to create a BEL namespace with HMDB disease names.

    :param file: file to which the namespace should be written. If None it will be outputted in stdout
    :param values: Values that should be part of the namespace. here biofluids.
    """
    if values is None:
        values = get_hmdb_diseases()

    write_namespace(
        namespace_name='Human Metabolome Database Diseases',
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
