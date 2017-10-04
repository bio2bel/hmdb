Enrich BEL graphs
=================
In the current build it is possible to enrich BEL graphs containing metabolites with associated
disease or protein information and to enrich BEL graphs containing disease or protein information with associated metabolites.
This can be done with the functions further explained in `BEL Serialization`_

.. _BEL Serialization: bel_serialization.html

1. Create a local HMDB version
------------------------------
explained here_. The Manager object is needed in later steps.

.. _here: set_up_hmdb.html

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
