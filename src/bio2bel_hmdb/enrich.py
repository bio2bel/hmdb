# -*- coding: utf-8 -*-

import logging

from pybel_tools import pipeline
from bio2bel_hmdb.manager import Manager
from pybel.constants import *
from bio2bel_hmdb.create_namespace import write_belns

log = logging.getLogger(__name__)


@pipeline.in_place_mutator
def enrich_metabolites_proteins(graph, connection=None):
    """Adds  in the graph

    :param pybel.BELGraph graph: A BEL graph
    """

    m = Manager.ensure(connection)
    write_belns()

    for node, data in graph.nodes(data=True):
        if data[FUNCTION] != ABUNDANCE and data[FUNCTION] != PROTEIN:
            continue

        if NAMESPACE not in data:
            continue

        if data[NAMESPACE] == 'HMDB':
            metabolite_protein_interactions = m.query_associated_proteins(data[NAME])

        else:
            log.warning("Unable to map namespace: %s", data[NAMESPACE])
            continue

        if metabolite_protein_interactions is None:
            log.warning("Unable to find node: %s", node)
            continue

        for association in metabolite_protein_interactions:
            protein_data = association.protein.serialize_to_bel()
            protein_tuple = graph.add_node_from_data(protein_data)

            graph.add_edge(protein_tuple, node, attr_dict={
                RELATION: ASSOCIATION,
                EVIDENCE: None,
                CITATION: {
                    CITATION_TYPE: None,
                    CITATION_REFERENCE: None,
                },
                ANNOTATIONS: {
                    'name': association.protein.name,
                    'protein_type': association.protein.protein_type
                }
            })