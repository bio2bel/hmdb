# -*- coding: utf-8 -*-

import logging

from pybel_tools import pipeline
from bio2bel_hmdb.manager import Manager
from pybel.constants import *

log = logging.getLogger(__name__)


@pipeline.in_place_mutator
def enrich_metabolites_proteins(graph, connection=None):
    """Enriches a given BEL graph, which includes metabolites with proteins, that are associated to the metabolites.

    :param pybel.BELGraph graph: A BEL graph
    :param str connection: connection for the manager used to connect to a database
    """

    m = Manager.ensure(connection)

    for node, data in graph.nodes(data=True):
        if data[FUNCTION] != ABUNDANCE:
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


@pipeline.in_place_mutator
def enrich_metabolites_diseases(graph, connection=None):
    """Enriches a given BEL graph, which includes metabolites with diseases, to which the metabolites are associated.

    :param pybel.BELGraph graph: A BEL graph
    :param str connection: connection for the manager used to connect to a database
    """

    m = Manager.ensure(connection)

    for node, data in graph.nodes(data=True):
        if data[FUNCTION] != ABUNDANCE:
            continue

        if NAMESPACE not in data:
            continue

        if data[NAMESPACE] == 'HMDB':
            metabolite_disease_interactions = m.query_associated_diseases(data[NAME])

        else:
            log.warning("Unable to map namespace: %s", data[NAMESPACE])
            continue

        if metabolite_disease_interactions is None:
            log.warning("Unable to find node: %s", node)
            continue

        # add edges and collect all the references for this edge
        i = 0
        while i < len(metabolite_disease_interactions):
            association = metabolite_disease_interactions[i]
            references = []  # list for storing the reference articles
            old_disease = association.disease

            while True:  # collect the references for the metabolite disease interaction
                try:
                    if old_disease != metabolite_disease_interactions[i].disease:
                        break  # break if disease has changed
                    references.append(metabolite_disease_interactions[i].reference.pubmed_id)
                    i += 1
                except IndexError:
                    break

            # add disease node and construct edge
            disease_data = association.disease.serialize_to_bel()
            disease_tuple = graph.add_node_from_data(disease_data)
            graph.add_edge(disease_tuple, node, attr_dict={
                RELATION: ASSOCIATION,
                EVIDENCE: None,
                CITATION: {
                    CITATION_TYPE: CITATION_TYPE_PUBMED,
                    CITATION_REFERENCE: references[0],
                },
                ANNOTATIONS: {
                    'omim_id': association.disease.omim_id,
                    'additional_references': references[1::]
                }
            })
