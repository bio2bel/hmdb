# -*- coding: utf-8 -*-

"""
Enrich BEL graphs
=================
In the current build it is possible to enrich BEL graphs containing metabolites with associated
disease or protein information and to enrich BEL graphs containing disease or protein information with associated metabolites.
This can be done with the functions further explained in `BEL Serialization`_

.. _BEL Serialization: bel_serialization.html

2. Enriching BEL graphs
-----------------------

Using an BEL graph with metabolites (represented using the `HMDB namespace`_) it can be enriched with disease and protein information from HMDB.

.. _HMDB namespace: construct_namspaces.html

2.1 Metabolites-Proteins
~~~~~~~~~~~~~~~~~~~~~~~~
For a graph containing metabolites:

>>> enrich_metabolites_proteins(bel_graph, manager)

The result of this will be a BEL graph which now includes relations between the metabolites and proteins.

For a graph containing proteins (named using uniprot identifiers):

>>> enrich_proteins_metabolites(bel_graph, manager)

This will result in a BEL graph where the proteins are linked to associated metabolites.

2.2 Metabolites-Diseases
~~~~~~~~~~~~~~~~~~~~~~~~
For a graph containing metabolites:

>>> enrich_metabolites_diseases(bel_graph, manager)

The result of this will be a BEL graph which now includes relations between the metabolites and diseases.

For a graph containing diseases (named using HMDB identifiers):

>>> enrich_diseases_metabolites(bel_graph, manager)

This will result in a BEL graph where the diseases are linked to associated metabolites.
"""

import logging
from typing import Optional

from pybel import BELGraph
from pybel.constants import (
    ABUNDANCE, ANNOTATIONS, ASSOCIATION, CITATION, CITATION_REFERENCE, CITATION_TYPE, CITATION_TYPE_PUBMED, EVIDENCE,
    FUNCTION, NAME, NAMESPACE, PATHOLOGY, PROTEIN, RELATION,
)
from pybel.struct.pipeline.decorators import in_place_transformation
from .manager import Manager

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
@in_place_transformation
def enrich_metabolites_proteins(graph: BELGraph, manager: Optional[Manager] = None):
    """Enrich a given BEL graph, which includes metabolites with proteins, that are associated to the metabolites."""
    if manager is None:
        manager = Manager()

    for node in list(graph):
        if _check_namespaces(node, ABUNDANCE, 'HMDB'):
            metabolite_protein_interactions = manager.query_metabolite_associated_proteins(node[NAME])
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


@in_place_transformation
def enrich_proteins_metabolites(graph: BELGraph, manager: Optional[Manager] = None):
    """Enrich a given BEL graph, which includes uniprot proteins with HMDB metabolites,
    that are associated to the proteins.
    """
    if manager is None:
        manager = Manager()

    for node in list(graph):
        if _check_namespaces(node, PROTEIN, 'UP'):
            protein_metabolite_interactions = manager.query_protein_associated_metabolites(node[NAME])
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
@in_place_transformation
def enrich_metabolites_diseases(graph: BELGraph, manager: Optional[Manager] = None):
    """Enrich a given BEL graph, which includes metabolites with diseases, to which the metabolites are associated."""
    if manager is None:
        manager = Manager()

    for data in list(graph):
        if _check_namespaces(data, ABUNDANCE, 'HMDB'):
            metabolite_disease_interactions = manager.query_metabolite_associated_diseases(data[NAME])
        else:
            continue

        if metabolite_disease_interactions is None:
            log.warning("Unable to find node: %s", data)
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
            graph.add_edge(disease_tuple, data, attr_dict={
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


@in_place_transformation
def enrich_diseases_metabolites(graph: BELGraph, manager: Optional[Manager] = None):
    """Enrich a given BEL graph, which includes HMDB diseases with HMDB metabolites, which are associated to the
    diseases."""
    if manager is None:
        manager = Manager()

    for data in list(graph):
        if _check_namespaces(data, PATHOLOGY, 'HMDB_D'):
            disease_metabolite_interactions = manager.query_disease_associated_metabolites(data[NAME])
        else:
            continue

        if not disease_metabolite_interactions:
            log.warning("Unable to find node: %s", data)
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
            graph.add_edge(metabolite_tuple, data, attr_dict={
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
