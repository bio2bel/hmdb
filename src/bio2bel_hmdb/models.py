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
    accession = Column(String, nullable=False)
    formula = Column(String, nullable=False)
    mol_weight = Column(Float, nullable=True)
    iupac = Column(String, nullable=False)
    trivial = Column(String, nullable=True)
    cas_id = Column(String, nullable=True)
    smiles = Column(String, nullable=True)
    inchi = Column(String, nullable=True)
    inchi_key = Column(String, nullable=True)

    biofluids = relationship('')


class Biofluid_loc(Base):
    """possible biofluids"""
    __tablename__ = "biofluid location"

    id = Column(Integer, primary_key=True)
    biofluid = Column(String, nullable=False)


class Substituents(Base):
    """Stores the different substituents"""
    __tablename__ = "substituents"

    id = Column(Integer, primary_key=True)
    substituent = Column(String, nullable=False)


class Cellular_loc(Base):
    """Stores the possible cellular locations"""
    __tablename__ = "cellular location"

    id = Column(Integer, primary_key=True)
    cellular_loc = Column(String, nullable=False)


class Tissues(Base):
    """Stores the possible tissues"""
    __tablename__ = "tissues"

    id = Column(Integer, primary_key=True)
    tissue = Column(String, nullable=False)
