# -*- coding: utf-8 -*-

"""
Work in progress:
- add missing tables
- add foreign keys and back population between tables
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Metabolite(Base):
    """Table which stores the metabolite and its descriptive information."""
    __tablename__ = "metabolite"

    id = Column(Integer, primary_key=True)
    version = Column(String, nullable=False, doc="Current version listing that metabolite")
    creation_date = Column(String, nullable=False, doc="Date when the metabolite was included into HMDB")
    update_date = Column(String, nullable=False, doc="Date when the entry was last updated")
    accession = Column(String, nullable=False, unique=True, doc="Accession ID for the metabolite")
    name = Column(String, nullable=True, doc="Name of the metabolite")
    description = Column(String, nullable=True, doc="Description including some information about the metabolite")
    chemical_formula = Column(String, nullable=False, doc="Chemical formula of the metabolite")
    average_molecular_weight = Column(Float, nullable=True, doc="Average molecular weight of the metabolite")
    monisotopic_molecular_weight = Column(Float, nullable=True, doc="Monisotopic weight of the molecule")
    iupac_name = Column(String, nullable=False, doc="IUPAC name of the metabolite")
    traditional_iupac = Column(String, nullable=True, doc="")
    trivial = Column(String, nullable=True, doc="Trivial name of the metabolite")
    cas_registry_number = Column(String, nullable=True, doc="Cas registry number of the metabolite")
    smiles = Column(String, nullable=True, doc="Smiles representation of the metabolite")
    inchi = Column(String, nullable=True, doc="Inchi of the metabolite")
    inchikey = Column(String, nullable=True, doc="Inchikey of the metabolite")
    state = Column(String, nullable=True, doc="Aggregate state of the metabolite")
    drugbank_id = Column(String, nullable=True, doc="Drugbank ID of the metabolite")
    drugbank_metabolite_id = Column(String, nullable=True, doc="Drugbank metabolite ID of the metabolite")
    phenol_explorer_compound_id = Column(String, nullable=True, doc="Phenol explorer compound ID of the metabolite")
    phenol_explorer_metabolite_id = Column(String, nullable=True, doc="Phenol explorer metabolite ID of the metabolite")
    foodb_id = Column(String, nullable=True, doc="FooDB ID of the metabolite")
    knapsack_id = Column(String, nullable=True, doc="Knapsack ID of the metabolite")
    chemspider_id = Column(String, nullable=True, doc="Chemspider ID of the metabolite")
    kegg_id = Column(String, nullable=True, doc="KEGG ID of the metabolite")
    biocyc_id = Column(String, nullable=True, doc="BioCyc ID of the metabolite")
    bigg_id = Column(String, nullable=True, doc="Bigg ID of the metabolite")
    wikipedia = Column(String, nullable=True, doc="Wikipedia ID of the metabolite")
    nugowiki = Column(String, nullable=True, doc="NukoWiki ID of the metabolite")
    metagene = Column(String, nullable=True, doc="Metagene ID of the metabolite")
    metlin_id = Column(String, nullable=True, doc="Metlin ID of the metabolite")
    pubchem_compound_id = Column(String, nullable=True, doc="PubChem compound ID of the metabolite")
    het_id = Column(String, nullable=True, doc="Het ID of the metabolite")
    chebi_id = Column(String, nullable=True, doc="Chebi ID of the metabolite")
    synthesis_reference = Column(String, nullable=True, doc="Synthesis reference citation of the metabolite")

class Biofluids(Base):
    """Table storing the different biofluids"""
    __tablename__ = "biofluids"

    id = Column(Integer, primary_key=True)
    biofluid = Column(String, nullable=False, unique=True, doc="Biofluid in which metabolites are found")

class MetaboliteBiofluid(Base):
    """Table representing the Metabolite and Biofluid relations"""
    __tablename__ = "metabolite_biofluid"

    id = Column(Integer, primary_key=True)
    metabolite_id = Column(Integer, ForeignKey("metabolite.id"))
    metabolite = relationship("Metabolite", backref="biofluid")
    biofluid_id = Column(Integer, ForeignKey("biofluids.id"))
    biofluid = relationship("Biofluids", backref="metabolite")
