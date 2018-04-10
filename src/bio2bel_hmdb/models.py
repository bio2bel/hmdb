# -*- coding: utf-8 -*-

"""The data model for the local HMDB version consists of 22 different tables that represent the relations found in the
original HMDB data.
"""

from pybel.dsl import abundance, pathology, protein
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

HMDB_ID = 'HMDB'
HMDB_DISEASE = 'HMDB_D'
UNIPROT = 'UP'

Base = declarative_base()


class Metabolite(Base):
    """Table which stores the metabolites and all the information provided about them in HMDB."""
    __tablename__ = "metabolite"

    id = Column(Integer, primary_key=True)
    version = Column(String(255), nullable=False, doc="Current version listing that metabolite")
    creation_date = Column(String(255), nullable=False, doc="Date when the metabolite was included into HMDB")
    update_date = Column(String(255), nullable=False, doc="Date when the entry was last updated")
    accession = Column(String(255), nullable=False, unique=True, doc="Accession ID for the metabolite")
    name = Column(String(255), nullable=True, doc="Name of the metabolite")
    description = Column(String(255), nullable=True, doc="Description including some information about the metabolite")
    chemical_formula = Column(String(255), nullable=False, doc="Chemical formula of the metabolite")
    average_molecular_weight = Column(Float, nullable=True, doc="Average molecular weight of the metabolite")
    monisotopic_molecular_weight = Column(Float, nullable=True, doc="Monisotopic weight of the molecule")
    iupac_name = Column(String(255), nullable=False, doc="IUPAC name of the metabolite")
    traditional_iupac = Column(String(255), nullable=True, doc="")
    trivial = Column(String(255), nullable=True, doc="Trivial name of the metabolite")
    cas_registry_number = Column(String(255), nullable=True, doc="Cas registry number of the metabolite")
    smiles = Column(String(255), nullable=True, doc="Smiles representation of the metabolite")
    inchi = Column(String(255), nullable=True, doc="Inchi of the metabolite")
    inchikey = Column(String(255), nullable=True, doc="InCHI key of the metabolite")
    state = Column(String(255), nullable=True, doc="Aggregate state of the metabolite")
    drugbank_id = Column(String(255), nullable=True, doc="DrugBank identifier of the metabolite")
    drugbank_metabolite_id = Column(String(255), nullable=True, doc="Drugbank metabolite ID of the metabolite")
    phenol_explorer_compound_id = Column(String(255), nullable=True, doc="Phenol explorer compound ID of the metabolite")
    phenol_explorer_metabolite_id = Column(String(255), nullable=True, doc="Phenol explorer metabolite ID of the metabolite")
    foodb_id = Column(String(255), nullable=True, doc="FooDB ID of the metabolite")
    knapsack_id = Column(String(255), nullable=True, doc="Knapsack ID of the metabolite")
    chemspider_id = Column(String(255), nullable=True, doc="Chemspider ID of the metabolite")
    kegg_id = Column(String(255), nullable=True, doc="KEGG ID of the metabolite")
    biocyc_id = Column(String(255), nullable=True, doc="BioCyc ID of the metabolite")
    bigg_id = Column(String(255), nullable=True, doc="Bigg ID of the metabolite")
    wikipedia = Column(String(255), nullable=True, doc="Wikipedia name of the metabolite")
    nugowiki = Column(String(255), nullable=True, doc="NukoWiki ID of the metabolite")
    metagene = Column(String(255), nullable=True, doc="Metagene ID of the metabolite")
    metlin_id = Column(String(255), nullable=True, doc="Metlin ID of the metabolite")
    pubchem_compound_id = Column(String(255), nullable=True, doc="PubChem compound ID of the metabolite")
    het_id = Column(String(255), nullable=True, doc="Het ID of the metabolite")
    chebi_id = Column(String(255), nullable=True, doc="ChEBI identifier of the metabolite")
    synthesis_reference = Column(String(255), nullable=True, doc="Synthesis reference citation of the metabolite")

    def serialize_to_bel(self):
        """Function to serialize a metabolite object to a PyBEL node data dictionary.

        :rtype: pybel.dsl.abundance
        """
        return abundance(namespace=HMDB_ID, name=str(self.accession))


class SecondaryAccessions(Base):
    """Table storing the different synonyms of metabolites."""
    __tablename__ = "secondary_accessions"

    id = Column(Integer, primary_key=True)
    secondary_accession = Column(String(255), nullable=False, unique=True, doc="Other accession numbers for the metabolite")
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="secondary_accessions")


class Biofluids(Base):
    """Table storing the different biofluids"""
    __tablename__ = "biofluids"

    id = Column(Integer, primary_key=True)
    biofluid = Column(String(255), nullable=False, unique=True, doc="Biofluid in which metabolites are found")


class MetaboliteBiofluid(Base):
    """Table representing the Metabolite and Biofluid relations"""
    __tablename__ = "metabolite_biofluid"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="biofluids")
    biofluid_id = Column(Integer, ForeignKey("biofluids.id"))
    biofluid = relationship("Biofluids", backref="metabolites")


class Synonyms(Base):
    """Table storing the synonyms of metabolites."""
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True)
    synonym = Column(String(255), nullable=False, unique=True, doc="Synonym for the metabolite")
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="synonyms")


class MetaboliteTissues(Base):
    """Table storing the different relations between tissues and metabolites"""
    __tablename__ = "metabolite_tissues"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="tissues")
    tissue_id = Column(Integer, ForeignKey("tissues.id"))
    tissue = relationship("Tissues", backref="metabolites")


class Tissues(Base):
    """Table storing the different tissues"""
    __tablename__ = "tissues"

    id = Column(Integer, primary_key=True)
    tissue = Column(String(255), nullable=False, unique=True, doc="Tissue type")


class MetabolitePathways(Base):
    """Table storing the different relations between pathways and metabolites"""
    __tablename__ = "metabolite_pathways"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="pathways")
    pathway_id = Column(Integer, ForeignKey("pathways.id"))
    pathway = relationship("Pathways", backref="metabolites")


class Pathways(Base):
    """Table storing the different tissues"""
    __tablename__ = "pathways"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True, unique=True, doc="Name of the pathway.")
    smpdb_id = Column(String(255), nullable=True, unique=False, doc="SMPDB identifier of the pathway.")
    kegg_map_id = Column(String(255), nullable=True, unique=False, doc="KEGG Map identifier of the pathway.")


class Proteins(Base):
    """Table to store the protein information"""
    __tablename__ = "proteins"

    id = Column(Integer, primary_key=True)
    protein_accession = Column(String(255), nullable=False, unique=True, doc="HMDB accession number for the protein")
    name = Column(String(255), nullable=False)
    uniprot_id = Column(String(255), nullable=True, doc="UniProt identifier of the protein")
    gene_name = Column(String(255), nullable=True, doc="Gene name of the protein coding gene")
    protein_type = Column(String(255), nullable=True, doc="Protein type like 'enzyme' etc.")

    def serialize_to_bel(self):
        """Function to serialize a protein object to a PyBEL node data dictionary.

        :rtype: pybel.dsl.protein
        """
        return protein(namespace=UNIPROT, name=str(self.uniprot_id))


class MetaboliteProteins(Base):
    """Table representing the many to many relationship between metabolites and proteins"""
    __tablename__ = "metabolite_proteins"

    id = Column(Integer, primary_key=True)

    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="proteins")

    protein_id = Column(Integer, ForeignKey("proteins.id"))
    protein = relationship("Proteins", backref="metabolites")


class References(Base):
    """Table storing literature references"""
    __tablename__ = "references"

    id = Column(Integer, primary_key=True)
    reference_text = Column(String(255), nullable=False, unique=True, doc="Citation of the reference article")
    pubmed_id = Column(String(255), nullable=True, unique=True, doc="PubMed identifier of the article")


class MetaboliteReferences(Base):
    """Table representing the many to many relationship between metabolites and references"""
    __tablename__ = "metabolite_references"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="references")
    reference_id = Column(Integer, ForeignKey("references.id"))
    reference = relationship("References", backref="metabolites")


class Diseases(Base):
    """Table storing the diseases and their ids"""
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, doc="Name of the disease")
    omim_id = Column(String(255), nullable=True, doc="OMIM identifier associated with the disease")
    dion = Column(String(255), nullable=True, doc="Disease Ontology name for this disease. Found using string matching")
    hpo = Column(String(255), nullable=True,
                 doc="Humand Phenotype Ontology name for this disease. Found using string matching")
    mesh_diseases = Column(String(255), nullable=True,
                           doc="MeSH Disease name for this disease. Found using string matching")

    def serialize_to_bel(self):
        """Function to serialize a disease object to a PyBEL node data dictionary.

        :rtype: pybel.dsl.pathology
        """
        return pathology(namespace=HMDB_DISEASE, name=str(self.name))


class MetaboliteDiseasesReferences(Base):
    """Table storing the relations between disease and metabolite"""
    __tablename__ = "metabolite_disease"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="diseases")
    disease_id = Column(Integer, ForeignKey("diseases.id"))
    disease = relationship("Diseases", backref="metabolites")
    reference_id = Column(Integer, ForeignKey("references.id"))
    reference = relationship("References", backref="diseases")


class PropertyValues(Base):
    """Table storing the values of chemical properties.
    Not used for BEL enrichment"""
    __tablename__ = "property_values"

    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False, unique=True,
                   doc="value of a chemical property (e.g. logp) that will be linked to the properts and metabolites")


class PropertyKinds(Base):
    """Table storing the 'kind' of chemical properties e.g. logP.
    Not used for BEL enrichment"""
    __tablename__ = "property_kinds"

    id = Column(Integer, primary_key=True)
    kind = Column(String(255), nullable=False, unique=True,
                  doc="the 'kind' of chemical properties e.g. logP, melting point etc")


class PropertySource(Base):
    """Table storing the sources of properties e.g. software like 'ALOGPS'.
    Not used for BEL enrichment"""
    __tablename__ = "property_source"

    id = Column(Integer, primary_key=True)
    source = Column(String(255), nullable=False, unique=True)


class CellularLocations(Base):
    """Table for storing the cellular location GO annotations"""
    __tablename__ = "cellular_locations"

    id = Column(Integer, primary_key=True)
    cellular_location = Column(String(255), nullable=False, unique=True)


class Biofunctions(Base):
    """Table for storing the 'biofunctions' annotations"""
    __tablename__ = "biofunctions"

    id = Column(Integer, primary_key=True)
    biofunction = Column(String(255), nullable=False, unique=True)


class MetaboliteCellularLocations(Base):
    """Table storing the many to many relations between metabolites and cellular location GO annotations"""
    __tablename__ = "metabolite_cellular_locations"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="cellular_locations")
    cellular_location_id = Column(Integer, ForeignKey("cellular_locations.id"))
    cellular_location = relationship("CellularLocations", backref="metabolites")


class MetaboliteBiofunctions(Base):
    """Table storing the many to many relations between metabolites and cellular location GO annotations"""
    __tablename__ = "metabolite_biofunctions"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="biofunctions")
    biofunctions_id = Column(Integer, ForeignKey("biofunctions.id"))
    biofunction = relationship("Biofunctions", backref="metabolites")
