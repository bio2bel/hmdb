# -*- coding: utf-8 -*-

"""The Manager is a key component of HMDB. This class is used to create, populate and query the local HMDB version."""

import logging
from typing import List, Mapping, Optional

from bel_resources import get_bel_resource
from bio2bel import AbstractManager
from tqdm import tqdm

from .constants import DOID, HP, MESHD, MODULE_NAME, ONTOLOGIES, ONTOLOGY_NAMESPACES
from .models import (
    Base, Biofluid, Biofunction, CellularLocation, Disease, Metabolite, MetaboliteBiofluid, MetaboliteCellularLocation,
    MetaboliteDiseaseReference, MetabolitePathway, MetaboliteProtein, MetaboliteReference,
    MetaboliteSynonym, MetaboliteTissue, Pathway, Protein, Reference, SecondaryAccession, Tissue,
)
from .parser import get_data

__all__ = [
    'Manager',
]

log = logging.getLogger(__name__)


class Manager(AbstractManager):
    """Managers handle the database construction, population and querying."""

    module_name = MODULE_NAME
    flask_admin_models = [Metabolite, Disease, Protein, Pathway, Biofluid]
    _base = Base

    def is_populated(self) -> bool:
        """Check if the database is already populated."""
        return 0 < self.count_metabolites()

    @staticmethod
    def _get_tag(element_tag) -> str:
        """Delete the XML namespace prefix when calling element.tag

        :param element_tag: tag attribute of an XML element
        """
        return element_tag.split("}")[1]

    def _populate_with_1_layer_elements(
            self,
            element,
            metabolite_instance,
            instance_dict,
            table,
            relation_table,
            column_name: str,
    ):
        """Parse and populate database with metabolite elements, which themselfes have one more layer.

        :param element: the current parent XML element. E.g. "pathways" where the children would have the tag "pathway".
        :param models.Metabolite metabolite_instance: metabolite object which is associated with the instances (e.g. is
                                                      involved in that "pathway")
        :param dict instance_dict: dictionary which tracks if the found instance is already present in the table and can
                                   then refer to it
        :param class table: sqlalchemy class to which the instances belong. E.g. "Pathways"
        :param class relation_table: sqlalchemy class which stores the many to many relation between the instances and
                                     the metabolites
        :param column_name: Name of the column in the relation tables which does not represent the metabolite.
                                e.g. reference, pathway etc
        :rtype: dict
        """
        for instance_element in element:
            instance_dict_key = instance_element.text

            if instance_dict_key not in instance_dict:  # check if instance is already in table
                new_instance_dict = {column_name: instance_dict_key}
                instance_dict[instance_dict_key] = table(**new_instance_dict)
                self.session.add(instance_dict[instance_dict_key])

            # create metabolite-instance relation object
            new_meta_rel_dict = {"metabolite": metabolite_instance, column_name: instance_dict[instance_dict_key]}
            self.session.add(relation_table(**new_meta_rel_dict))
        return instance_dict

    def _populate_with_2_layer_elements(
            self,
            element,
            metabolite_instance,
            instance_dict,
            table,
            relation_table,
            column,
            instance_dict_key=None,
            metabolite_column='metabolite',
    ):
        """Parse and populate database with metabolite elements, which themselves have two more layers.

        :param element: the current parent XML element. E.g. "pathways" where the children would have the tag "pathway".
        :param models.Metabolite metabolite_instance: metabolite object which is associated with the instances (e.g. is
        involved in that "pathway")
        :param dict instance_dict: dictionary which tracks if the found instance is already present in the table and can
        then refer to it
        :param type table: sqlalchemy class to which the instances belong. E.g. "Pathways"
        :param type relation_table: sqlalchemy class which stores the many to many relation between the instances and
        the metabolites
        :param str column: column name of the relation table which is not the metabolite
        :param str instance_dict_key: String which is used as the key for the instance_dict. (to ensure uniqueness in
        the instance_dict)
        :param str metabolite_column: column of the relation table which represents the foreignkey to the main table.
        In our database model the Metabolite table.
        :rtype: dict
        """
        if instance_dict_key is None and len(element) > 0:
            instance_dict_key = self._get_tag(element[0][0].tag)

        for instance_element in element:
            # build pathway object dict to create pathway object
            instance_object_dict = {}

            # create pathway instance
            for instance_sub_element in instance_element:
                cutted_pathway_tag = self._get_tag(instance_sub_element.tag)
                instance_object_dict[cutted_pathway_tag] = instance_sub_element.text

            # add MetabolitePathway relation and continue with next pathway if pathway already present in Pathways
            if instance_object_dict[instance_dict_key] in instance_dict:
                new_meta_rel_dict = {
                    metabolite_column: metabolite_instance,
                    column: instance_dict[instance_object_dict[instance_dict_key]]
                }
                new_meta_rel = relation_table(**new_meta_rel_dict)
                self.session.add(new_meta_rel)
                continue

            instance_dict[instance_object_dict[instance_dict_key]] = table(**instance_object_dict)
            self.session.add(instance_dict[instance_object_dict[instance_dict_key]])

            new_meta_rel_dict = {
                metabolite_column: metabolite_instance,
                column: instance_dict[instance_object_dict[instance_dict_key]]
            }
            new_meta_rel = relation_table(**new_meta_rel_dict)
            self.session.add(new_meta_rel)

        return instance_dict

    def _populate_diseases(
            self,
            element,
            references_dict,
            diseases_dict,
            metabolite_instance,
            disease_ontologies=None,
            map_dis=True,
    ):
        """Populates the database with disease and related reference information.

        :param element: Element object from the xml ElementTree
        :param dict references_dict: Dictionary to keep track of which references are already in the database
        :param dict diseases_dict: Dictionary to keep track of which diseases are already in the database
        :param models.Metabolite metabolite_instance: Metabolite object to which the diseases and references are related
        :param boolean map_dis: If True the HMDB disease names will be mapped to different ontologies.
        :rtype: dict, dict
        """
        for disease_element in element:
            disease_instance = Disease()

            for disease_sub_element in disease_element:
                dtag = self._get_tag(disease_sub_element.tag)

                if dtag != "references":
                    setattr(disease_instance, dtag, disease_sub_element.text)
                    continue

                if disease_instance.name not in diseases_dict:  # add disease instance if not already in table
                    # map to different disease ontologies if map is True
                    if map_dis:
                        disease_lower = disease_instance.name.lower()  # for case insensitivity
                        for ontology in disease_ontologies:
                            if disease_lower not in disease_ontologies[ontology]:
                                continue

                            v = disease_ontologies[ontology][disease_lower]

                            if ontology == DOID:
                                setattr(disease_instance, 'dion', v)
                            elif ontology == HP:
                                setattr(disease_instance, 'hpo', v)
                            elif ontology == MESHD:
                                setattr(disease_instance, 'mesh_diseases', v)

                    diseases_dict[disease_instance.name] = disease_instance
                    self.session.add(disease_instance)

                for reference_element in disease_sub_element:
                    new_reference_object_dict = {}  # dict to check if reference is already presend in table

                    for reference_sub_element in reference_element:  # construct new reference object
                        reference_tag = self._get_tag(reference_sub_element.tag)
                        new_reference_object_dict[reference_tag] = reference_sub_element.text

                    # add if not already in reference table
                    if new_reference_object_dict['reference_text'] not in references_dict:
                        references_dict[new_reference_object_dict['reference_text']] = Reference(
                            **new_reference_object_dict)
                        self.session.add(references_dict[new_reference_object_dict['reference_text']])

                    rel_meta_dis_ref = MetaboliteDiseaseReference(
                        metabolite=metabolite_instance,
                        disease=diseases_dict[disease_instance.name],
                        reference=references_dict[new_reference_object_dict['reference_text']]
                    )
                    self.session.add(rel_meta_dis_ref)
        return references_dict, diseases_dict

    @staticmethod
    def _disease_ontology_dict(ontology: str) -> Mapping[str, str]:
        """Create a dictionary from the disease ontologies used for mapping HMDB disease names to those ontologies."""
        doid_path = ONTOLOGY_NAMESPACES[ontology]
        doid_ns = get_bel_resource(doid_path)
        return {value.lower(): value for value in doid_ns['Values']}

    def populate(self, source: Optional[str] = None, map_dis: bool = True, group_size: int = 500_000):
        """Populate the database with the HMDB data.

        :param source: Path to an .xml file. If None the whole HMDB will be downloaded and used for population.
        :param map_dis: Should diseases be mapped?
        """
        # construct sets for disease ontologies for mapping hmdb diseases
        if not map_dis:
            disease_ontologies = None
        else:
            disease_ontologies = {
                ontology: self._disease_ontology_dict(ontology)
                for ontology in ONTOLOGIES
            }

        # construct xml tree
        tree = get_data(source)
        root = tree.getroot()

        # dicts to check unique constraints for specific tables
        biofluids_dict = {}
        tissues_dict = {}
        pathways_dict = {}
        proteins_dict = {}
        references_dict = {}
        diseases_dict = {}
        # biofunctions_dict = {}
        cellular_locations_dict = {}

        # iterate through xml tree
        for i, elements in enumerate(tqdm(root, desc='HMDB Metabolite')):
            # create metabolite dict used to feed in main metabolite table
            metabolite = Metabolite()

            for element in elements:
                # delete namespace prefix
                tag = self._get_tag(element.tag)

                # handle wikipedia typo in xml tags
                if tag == "wikipidia":
                    log.warning("HMDB fixed the 'wikipidia' tag to 'wikipedia'. Change code.")
                    tag = "wikipedia"

                if tag == "secondary_accessions":
                    self.session.add_all([
                        SecondaryAccession(
                            metabolite=metabolite,
                            secondary_accession=secondary_accession_element.text
                        )
                        for secondary_accession_element in element
                    ])

                elif tag == "synonyms":
                    synonyms = {
                        synonym_element.text
                        for synonym_element in element
                    }
                    self.session.add_all([
                        MetaboliteSynonym(
                            metabolite=metabolite,
                            synonym=synonym,
                        )
                        for synonym in synonyms
                    ])

                elif tag == "taxonomy":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "ontology":
                    continue

                elif tag == "cellular_locations":
                    cellular_locations_dict = self._populate_with_1_layer_elements(
                        element,
                        metabolite,
                        cellular_locations_dict,
                        CellularLocation,
                        MetaboliteCellularLocation,
                        "cellular_location"
                    )

                elif tag == "experimental_properties":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "predicted_properties":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "spectra":  # will not be processed since the corresponding database is down
                    continue

                elif tag == "biospecimen_locations":
                    biofluids_dict = self._populate_with_1_layer_elements(
                        element,
                        metabolite,
                        biofluids_dict,
                        Biofluid,
                        MetaboliteBiofluid,
                        'biofluid',
                    )

                elif tag == "tissue_locations":
                    tissues_dict = self._populate_with_1_layer_elements(
                        element,
                        metabolite,
                        tissues_dict,
                        Tissue,
                        MetaboliteTissue,
                        'tissue',
                    )

                elif tag == "pathways":
                    pathways_dict = self._populate_with_2_layer_elements(
                        element,
                        metabolite,
                        pathways_dict,
                        Pathway,
                        MetabolitePathway,
                        'pathway',
                    )

                elif tag == "normal_concentrations":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "abnormal_concentrations":  # will be delayed to later versions since not important for BEL
                    continue

                elif tag == "diseases":
                    references_dict, diseases_dict = self._populate_diseases(
                        element,
                        references_dict,
                        diseases_dict,
                        metabolite,
                        disease_ontologies,
                        map_dis=map_dis,
                    )

                elif tag == "general_references":
                    references_dict = self._populate_with_2_layer_elements(
                        element,
                        metabolite,
                        references_dict,
                        Reference,
                        MetaboliteReference,
                        'reference',
                        "reference_text",
                    )

                elif tag == "protein_associations":
                    proteins_dict = self._populate_with_2_layer_elements(
                        element,
                        metabolite,
                        proteins_dict,
                        Protein,
                        MetaboliteProtein,
                        'protein',
                    )

                else:  # feed in main metabolite table
                    setattr(metabolite, tag, element.text)

            self.session.add(metabolite)

            if (i + 1) % group_size:
                log.warning('committing')
                self.session.commit()

        self.session.commit()

    def get_metabolite_by_accession(self, hmdb_metabolite_accession: str) -> Optional[Metabolite]:
        """Query the constructed HMDB database and extract a metabolite object.

        :param hmdb_metabolite_accession: HMDB metabolite identifier

        Example:

        >>> import bio2bel_hmdb
        >>> manager = bio2bel_hmdb.Manager()
        >>> manager.get_metabolite_by_accession("HMDB00072")
        """
        return self.session.query(Metabolite).filter(Metabolite.accession == hmdb_metabolite_accession).one_or_none()

    def query_metabolite_associated_proteins(self, hmdb_metabolite_id: str) -> Optional[List[Protein]]:
        """Query the constructed HMDB database to get the metabolite associated protein relations for BEL enrichment

        :param hmdb_metabolite_id: HMDB metabolite identifier
        """
        metabolite = self.get_metabolite_by_accession(hmdb_metabolite_id)
        if metabolite is not None:
            return metabolite.proteins

    def query_metabolite_associated_diseases(self, hmdb_metabolite_id: str) -> List[Disease]:
        """Query the constructed HMDB database to get the metabolite associated disease relations for BEL enrichment

        :param hmdb_metabolite_id: HMDB metabolite identifier
        """
        metabolite = self.get_metabolite_by_accession(hmdb_metabolite_id)
        return metabolite.diseases

    def query_disease_associated_metabolites(self, disease_name: str) -> List[Metabolite]:
        """Query function that returns a list of metabolite-disease interactions, which are associated to a disease.

        :param disease_name: HMDB disease name
        """
        return self.session.query(Disease).filter(Disease.name == disease_name).one_or_none().metabolites

    def query_protein_associated_metabolites(self, uniprot_id):
        """Query function that returns a list of metabolite-disease interactions, which are associated to a disease.

        :param str uniprot_id: uniprot identifier of a protein for which the associated metabolite relations should be
                                outputted
        :rtype: list
        """
        return self.session.query(Protein).filter(Protein.uniprot_id == uniprot_id).one_or_none().metabolites

    def get_hmdb_accession(self):
        """Create a list of all HMDB metabolite identifiers present in the database.

        :rtype: list
        """
        accessions = self.session.query(Metabolite.accession).all()
        if not accessions:
            log.warning("Database not populated. Please populate database before calling this function")

        return [a[0] for a in accessions]  # if anybody knows a better way of querying for a flat list. Please change.

    def get_hmdb_diseases(self):
        """Create a list of all disease names present in the database.

        :rtype: list
        """
        accessions = self.session.query(Disease.name).all()
        if not accessions:
            log.warning("Database not populated. Please populate database before calling this function")

        return [a for a, in accessions]

    def _get_models(self, interaction_table):
        """Extracts all interactions from the many to many interaction table.

        :param type interaction_table: Relation table from the database model. (e.g. MetaboliteProteins)
        :rtype: query
        """
        return self.session.query(interaction_table).all()

    def get_metabolite_disease_interactions(self) -> List[MetaboliteDiseaseReference]:
        return self._get_models(MetaboliteDiseaseReference)

    def get_metabolite_protein_interactions(self) -> List[MetaboliteProtein]:
        return self._get_models(MetaboliteProtein)

    def count_diseases(self) -> int:
        """Count the number of diseases in the database."""
        return self.session.query(Disease).count()

    def count_cellular_locations(self):
        """Count the number of cellular locations in the database."""
        return self.session.query(CellularLocation).count()

    def count_references(self):
        """Count the number of literature references in the database."""
        return self.session.query(Reference).count()

    def get_reference_by_pubmed_id(self, pubmed_id: str) -> Optional[Reference]:
        """Get a reference by its PubMed identifier if it exists.

        :param pubmed_id: The PubMed identifier to search
        """
        return self.session.query(Reference).filter(Reference.pubmed_id == pubmed_id).one_or_none()

    def count_proteins(self) -> int:
        """Count the number of proteins in the database."""
        return self.session.query(Protein).count()

    def count_biofunctions(self) -> int:
        """Count the number of biofunctions in the database."""
        return self.session.query(Biofunction).count()

    def count_metabolites(self) -> int:
        """Count the number of metabolites in the database."""
        return self._count_model(Metabolite)

    def count_pathways(self) -> int:
        """Count the number of pathways in the database."""
        return self._count_model(Pathway)

    def count_tissues(self) -> int:
        """Count the number of tissues in the database."""
        return self._count_model(Tissue)

    def summarize(self) -> Mapping[str, int]:
        """Summarize the contents of the database in a dictionary."""
        return dict(
            proteins=self.count_proteins(),
            diseases=self.count_diseases(),
            biofunctions=self.count_biofunctions(),
            references=self.count_references(),
            cellular_locations=self.count_cellular_locations(),
            metabolites=self.count_metabolites(),
            tissues=self.count_tissues(),
        )
