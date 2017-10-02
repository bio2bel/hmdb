# -*- coding: utf-8 -*-

from bio2bel_hmdb.constants import ONTOLOGIES
from bio2bel_hmdb.manager import Manager
from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL, NAMESPACE_DOMAIN_OTHER
from pybel_tools.definition_utils import write_namespace
from pybel_tools.resources import get_latest_arty_namespace
from pybel.utils import get_bel_resource


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


def construct_hmdb_disease_mapping(connection=None):
    """
    constructs a mapping of hmdb disease names to actually useful ontologies.

    :param str connection: Connection string to connect manager to a database. Can also directly be a manager.
    :rtype: dict, int
    """

    def check_ns(ns, terms):
        """
        download and extract values from an BEL namespace and create a mapping from the terms to the BEL namespaces,
        if the terms occur in the namespace.

        :param str ns: the name of the namespace which should be checked
        :param terms: a list of terms which should be searched for in the namespace
        and that will be mapped to the namespace
        :rtype doid_mapping: dict
        :rtype hmdb_diseases: list
        """

        # download latest version of the namespace
        doid_path = get_latest_arty_namespace(ns)
        doid_ns = get_bel_resource(doid_path)
        doid_values = {value.lower(): value for value in doid_ns['Values']}
        doid_mapping = {}
        i = 0
        while i < len(terms):
            d_lower = terms[i].lower()
            if d_lower in doid_values:
                doid_mapping[terms.pop(i)] = doid_values[d_lower]
                i -= 1
            i += 1
        return doid_mapping, terms

    m = Manager.ensure(connection)
    hmdb_diseases = m.get_hmdb_diseases()

    mapping = {}
    for ontology in ONTOLOGIES:
        # check if disease name exists in the ontology
        mapping[ontology], hmdb_diseases = check_ns(ontology, hmdb_diseases)

        if not hmdb_diseases:
            break

    return mapping, len(hmdb_diseases)
