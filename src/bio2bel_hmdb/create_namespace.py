# -*- coding: utf-8 -*-

from bio2bel_hmdb.constants import HMDB_SQLITE_PATH
from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite
from pybel.constants import NAMESPACE_DOMAIN_CHEMICAL
from pybel_tools.definition_utils import write_namespace
from tests.constants import text_xml_path


def get_hmdb_accession():
    """ """
    m = Manager(HMDB_SQLITE_PATH)

    accessions = m.session.query(Metabolite.accession).all()
    return [a[0] for a in accessions]  # if anybody knows a better way of querying for a flat list. Please change.


def write_belns(file=None, values=None):
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


if __name__ == '__main__':
    get_hmdb_accession()
