import logging

from pybel.utils import ensure_quotes
from pybel_tools.document_utils import write_boilerplate
from pybel_tools.resources import CONFIDENCE

from bio2bel_hmdb.constants import DISEASE_ONTOLOGY, HUMAN_PHENOTYPE_ONTOLOGY, MESH_DISEASES
from bio2bel_hmdb.models import MetaboliteProteins, MetaboliteDiseasesReferences


def write_interpro_tree_boilerplate(file=None):
    """
    writes the BEL document header to the file

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
            # FIXME
        },
        namespace_patterns={},
        annotations_dict={'Confidence': CONFIDENCE},
        annotations_patterns={},
        file=file
    )


def write_metabolites_proteins_bel(manager, file=None):
    """
    writes the metabolite-protein association relations found in HMDB into a BEL document.

    :param manager: Manager object connected to the local HMDB database
    :param file file: A writeable file or file like. Defaults to stdout
    """
    interactions = manager.get_interactions(MetaboliteProteins)

    for interaction in interactions:
        print('SET Citation = {"Human Metabolite Database"}', file=file)
        print('SET Evidence = "Database Entry"', file=file)
        print('SET Confidence = "Axiomatic"', file=file)

        protein = interaction.protein.uniprot_id
        metabolite = interaction.metabolite.accession
        write_bel_association('a', 'HMDB', metabolite, 'path', 'UP', protein, file)
        print('UNSET ALL', file=file)


def get_journal(interaction):
    """
    gets the journal name from the in HMDB provided reference strings.

    :param interaction: interaction_table object (e.g. MetaboliteProteins)
    :rtype: str
    """
    return interaction.reference.reference_text.split(".")[1]


def write_metabolites_diseases_bel(manager, file=None):
    """
    writes the metabolite-disease association relations found in HMDB into a BEL document.

    :param manager: Manager object connected to the local HMDB database
    :param file file: A writeable file or file like. Defaults to stdout
    """
    interactions = manager.get_interactions(MetaboliteDiseasesReferences)

    for interaction in interactions:
        if interaction.disease.dion is not None:
            disease_name = interaction.disease.dion
            dis_namespace = DISEASE_ONTOLOGY
        elif interaction.disease.hpo is not None:
            disease_name = interaction.disease.hpo
            dis_namespace = HUMAN_PHENOTYPE_ONTOLOGY
        elif interaction.disease.mesh_diseases is not None:
            disease_name = interaction.disease.mesh_diseases
            dis_namespace = MESH_DISEASES
        else:
            logging.warning('HMDB disease name is not found in disease ontologies. HMDB name is used.')
            dis_namespace = 'HMDB_D'
            disease_name = interaction.disease.name

        accession = interaction.metabolite.accession

        if interaction.reference.pubmed_id is None:
            citation = interaction.reference.reference_text
            print('SET Citation = {{"{}"}}'.format(citation), file=file)
        else:
            pubmed = interaction.reference.pubmed_id
            journal = get_journal(interaction)
            print('SET Citation = {{"PubMed", "{}", "{}"}}'.format(journal, pubmed))

        print('SET Evidence = "Database Entry"', file=file)
        print('SET Confidence = "Axiomatic"', file=file)
        print('SET Species = "9606”')
        print('SET Disease = "{}"'.format(disease_name))

        write_bel_association('a', 'HMDB', accession, 'path', dis_namespace, disease_name, file)
        print('UNSET ALL', file=file)


def write_bel_association(abundance1, namespace1, accession1, abundance2, namespace2, accession2, file=None):
    """
    prints a BEL association.

    :param str abundance1: Abundance of the subject
    :param str namespace1: Namespace of the subject
    :param str accession1: Identifier of the subject
    :param str abundance2: Abundance of the object
    :param str namespace2: Namespace of the object
    :param str accession2: Identifier of the object
    :param file file: A writeable file or file like. Defaults to stdout
    """
    print(
        '{}({}:{}) -- {}({}:{})'.format(
            ensure_quotes(abundance1),
            ensure_quotes(namespace1),
            ensure_quotes(accession1),
            ensure_quotes(abundance2),
            ensure_quotes(namespace2),
            ensure_quotes(accession2)
        ),
        file=file
    )

