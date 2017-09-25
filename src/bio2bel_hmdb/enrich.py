# -*- coding: utf-8 -*-

import logging

from pybel_tools import pipeline
from .manager import Manager
from pybel.constants import *
from .create_namespace import write_belns

log = logging.getLogger(__name__)


@pipeline.in_place_mutator
def enrich_metabolites(graph, connection=None):
    """Adds  in the graph

    :param pybel.BELGraph graph: A BEL graph
    """

    m = Manager.ensure(connection)
    write_belns()


    for node, data in graph.nodes_iter(data=True):
        if data[FUNCTION] != RNA:
            continue

        if NAMESPACE not in data:
            continue

        if data[NAMESPACE] == 'HGNC':
            target = m.query_target_by_hgnc_symbol(data[NAME])

        elif data[NAMESPACE] == 'EGID':
            target = m.query_target_by_entrez_id(data[NAME])

        else:
            log.warning("Unable to map namespace: %s", data[NAMESPACE])
            continue

        if target is None:
            log.warning("Unable to find node: %s", node)
            continue

        for interaction in target.interactions:
            mirna_data = interaction.mirna.serialize_to_bel()
            mirna_tuple = graph.add_node_from_data(mirna_data)
            graph.add_edge(mirna_tuple, node, attr_dict={
                RELATION: DIRECTLY_DECREASES,
                EVIDENCE: '...', #FIXME
                CITATION: {
                    CITATION_TYPE: CITATION_TYPE_PUBMED,
                    CITATION_REFERENCE: interaction.evidence.reference,
                },
                ANNOTATIONS: {
                    'Experiment': interaction.evidence.experiment,
                    'SupportType': interaction.evidence.support,
                }
            })

