from pybel.utils import ensure_quotes
from pybel_tools.document_utils import write_boilerplate
from pybel_tools.resources import CONFIDENCE


def write_interpro_tree_boilerplate(file=None):
    """Writes the BEL document header to the file
    :param file file: A writeable file or file like. Defaults to stdout
    """
    write_boilerplate(
        document_name='HMDB Enrichment',
        authors='Colin Birkenbihl, Charles Tapley Hoyt',
        contact='colin.birkenbihl@scai.fraunhofer.de',
        licenses='Creative Commons by 4.0',
        copyright='Copyright (c) 2017 Colin Birkenbihl, Charles Tapley Hoyt. All Rights Reserved.',
        description="""This BEL document represents relations from HMDB.""",
        namespace_dict={
            # FIXME,
        },
        namespace_patterns={},
        annotations_dict={'Confidence': CONFIDENCE},
        annotations_patterns={},
        file=file
    )


def write_interpro_tree_body(graph, file):
    """Creates the lines of BEL document that represents the InterPro tree
    :param networkx.DiGraph graph: A graph representing the InterPro tree from :func:`main`
    :param file file: A writeable file or file-like. Defaults to stdout.
    """
    print('SET Citation = {"PubMed","InterPro","27899635"}', file=file)
    print('SET Evidence = "InterPro Definitions"', file=file)
    print('SET Confidence = "Axiomatic"', file=file)

    for parent, child in graph.edges_iter():
        print(
            'a(HMDB:{}) -- p(UP:{})'.format(
                ensure_quotes(child),
                ensure_quotes(parent),
            ),
            file=file
        )

    print('UNSET ALL', file=file)


def write_interpro_tree(file=None, force_download=False):
    """Creates the entire BEL document representing the InterPro tree
    :param file file: A writeable file or file-like. Defaults to stdout.
    :param bool force_download: Should the data be re-downloaded?
    """
    graph = get_graph(force_download=force_download)
    write_interpro_tree_boilerplate(file)


write_interpro_tree_body(graph, file)
