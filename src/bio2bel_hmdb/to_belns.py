# -*- coding: utf-8 -*-

from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL, NAMESPACE_DOMAIN_OTHER
from pybel.resources.definitions import get_bel_resource, write_namespace

from .constants import ONTOLOGY_NAMESPACES
from .manager import Manager


def write_hmdb_id_ns(file=None, values=None, connection=None):
    """
    Create a BEL namespace with HMDB identifiers.

    :param file: file to which the namespace should be written. If None it will be outputted in stdout
    :param values: Values that should be part of the namespace. (HMDB identifiers)
    :param str connection: Connection string to connect manager to a database. Can also directly be a manager
    """

    m = Manager.ensure(connection)

    if values is None:
        values = m.get_hmdb_accession()

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


def write_hmdb_disease_ns(file=None, values=None, connection=None):
    """
    Create a BEL namespace with HMDB disease names.

    :param file: file to which the namespace should be written. If None it will be outputted in stdout
    :param values: Values that should be part of the namespace. (disease names)
    :param str connection: Connection string to connect manager to a database. Can also directly be a manager.
    """
    m = Manager.ensure(connection)

    if values is None:
        values = m.get_hmdb_diseases()

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

