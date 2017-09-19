# -*- coding: utf-8 -*-

"""
Work in progress:
- add missing tables
- add foreign keys and back population between tables
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Metabolite(Base):
    """Table which stores the metabolite and its descriptive information."""
    __tablename__ = "metabolite"

    id = Column(Integer, primary_key=True)
    version = Column(String, nullable=False)
    creation_date = Column(String, nullable=False)
    update_date = Column(String, nullable=False)
    accession = Column(String, nullable=False)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    chemical_formula = Column(String, nullable=False)
    average_molecular_weight = Column(Float, nullable=True)
    monisotopic_molecular_weight = Column(Float, nullable=True)
    iupac_name = Column(String, nullable=False)
    traditional_iupac = Column(String, nullable=True)
    trivial = Column(String, nullable=True)
    cas_registry_number = Column(String, nullable=True)
    smiles = Column(String, nullable=True)
    inchi = Column(String, nullable=True)
    inchikey = Column(String, nullable=True)
    state = Column(String, nullable=True)
    drugbank_id = Column(String, nullable=True)
    drugbank_metabolite_id = Column(String, nullable=True)
    phenol_explorer_compound_id = Column(String, nullable=True)
    phenol_explorer_metabolite_id = Column(String, nullable=True)
    foodb_id = Column(String, nullable=True)
    knapsack_id = Column(String, nullable=True)
    chemspider_id = Column(String, nullable=True)
    kegg_id = Column(String, nullable=True)
    biocyc_id = Column(String, nullable=True)
    bigg_id = Column(String, nullable=True)
    wikipedia = Column(String, nullable=True)
    nugowiki = Column(String, nullable=True)
    metagene = Column(String, nullable=True)
    metlin_id = Column(String, nullable=True)
    pubchem_compound_id = Column(String, nullable=True)
    het_id = Column(String, nullable=True)
    chebi_id = Column(String, nullable=True)
    synthesis_reference = Column(String, nullable=True)
