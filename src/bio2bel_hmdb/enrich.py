# -*- coding: utf-8 -*-

import logging

from pybel_tools import pipeline
from bio2bel_hmdb.manager import Manager
from pybel.constants import *

log = logging.getLogger(__name__)


def _check_namespaces(data, bel_function, bel_namespace):
    """Makes code more structured and reusable."""
    if data[FUNCTION] != bel_function:
        return False

    if NAMESPACE not in data:
        return False

    if data[NAMESPACE] == bel_namespace:
        return True

    elif data[NAMESPACE] != bel_namespace:
        log.warning("Unable to map namespace: %s", data[NAMESPACE])
        return False


# enrich proteins and metabolites
@pipeline.in_place_mutator
def enrich_metabolites_proteins(graph, connection=None):
    """Enriches a given BEL graph, which includes metabolites with proteins, that are associated to the metabolites.

    :param pybel.BELGraph graph: A BEL graph
    :param str connection: connection for the manager used to connect to a database
    """

    m = Manager.ensure(connection)

    for node, data in graph.nodes(data=True):
        if _check_namespaces(data, ABUNDANCE, 'HMDB'):
            metabolite_protein_interactions = m.query_metabolite_associated_proteins(data[NAME])
        else:
            continue

        if not metabolite_protein_interactions:
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
def enrich_proteins_metabolites(graph, connection=None):
    """Enriches a given BEL graph, which includes uniprot proteins with HMDB metabolites,
    that are associated to the proteins.

    :param pybel.BELGraph graph: A BEL graph
    :param str connection: connection for the manager used to connect to a database
    """

    m = Manager.ensure(connection)

    for node, data in graph.nodes(data=True):
        if _check_namespaces(data, PROTEIN, 'UP'):
            protein_metabolite_interactions = m.query_protein_associated_metabolites(data[NAME])
        else:
            continue

        if protein_metabolite_interactions is None:
            log.warning("Unable to find node: %s", node)
            continue

        for association in protein_metabolite_interactions:
            metabolite_data = association.metabolite.serialize_to_bel()
            metabolite_tuple = graph.add_node_from_data(metabolite_data)

            graph.add_edge(metabolite_tuple, node, attr_dict={
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


# enrich diseases and metabolites
@pipeline.in_place_mutator
def enrich_metabolites_diseases(graph, connection=None):
    """Enriches a given BEL graph, which includes metabolites with diseases, to which the metabolites are associated.

    :param pybel.BELGraph graph: A BEL graph
    :param str connection: connection for the manager used to connect to a database
    """

    m = Manager.ensure(connection)

    for node, data in graph.nodes(data=True):
        if _check_namespaces(data, ABUNDANCE, 'HMDB'):
            metabolite_disease_interactions = m.query_metabolite_associated_diseases(data[NAME])
        else:
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


@pipeline.in_place_mutator
def enrich_diseases_metabolites(graph, connection=None):
    """Enriches a given BEL graph, which includes HMDB diseases with HMDB metabolites, which are associated to the diseases.

    :param pybel.BELGraph graph: A BEL graph
    :param str connection: connection for the manager used to connect to a database
    """

    m = Manager.ensure(connection)

    for node, data in graph.nodes(data=True):
        if _check_namespaces(data, PATHOLOGY, 'HMDB_D'):
            disease_metabolite_interactions = m.query_disease_associated_metabolites(data[NAME])
        else:
            continue

        if not disease_metabolite_interactions:
            log.warning("Unable to find node: %s", node)
            continue

        # add edges and collect all the references for this edge
        i = 0
        while i < len(disease_metabolite_interactions):
            association = disease_metabolite_interactions[i]
            references = []  # list for storing the reference articles
            old_metabolite = association.metabolite

            while True:  # collect the references for the metabolite disease interaction
                try:
                    if old_metabolite != disease_metabolite_interactions[i].metabolite:
                        break  # break if disease has changed
                    references.append(disease_metabolite_interactions[i].reference.pubmed_id)
                    i += 1
                except IndexError:
                    break

            # add disease node and construct edge
            metabolite_data = association.metabolite.serialize_to_bel()
            metabolite_tuple = graph.add_node_from_data(metabolite_data)
            graph.add_edge(metabolite_tuple, node, attr_dict={
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
