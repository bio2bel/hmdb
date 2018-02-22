# -*- coding: utf-8 -*-

from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL, NAMESPACE_DOMAIN_OTHER
from pybel.resources.arty import get_latest_arty_namespace
from pybel.resources.definitions import get_bel_resource, write_namespace

from .constants import ONTOLOGIES
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


def construct_hmdb_disease_mapping(connection=None):
    """
    This function is depricated. The mappings are already in the disease table in the database.
    Function constructs a mapping of hmdb disease names to actually useful ontologies.

    :param str connection: Connection string to connect manager to a database. Can also directly be a manager.
    :return: 1. Dictionary with the mappings from HMDB to the other ontologies. Consists of 3 dictionaries, one for each ontology. In those dictionaries the keys are the HMDB terms and they map to the corresponding ontology terms.
        2. Number of HMDB diseases that could not be mapped to any of the other ontologies
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
    unmapped = len(hmdb_diseases)

    return mapping, unmapped
