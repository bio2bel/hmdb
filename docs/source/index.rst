.. hmdb documentation master file, created by
   sphinx-quickstart on Thu Sep 28 15:10:03 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the PyHMDB documentation!
====================================

PyHMDB is a package which allows the user to work with a local sqlite version of the Human Metabolome Database (HMDB).
Next to creating the local database there are also functions provided, which will enrich given Biological Expression Language (BEL) graphs with information about metabolites, proteins and diseases, that is present in HMDB.
HMDB BEL namespaces for these BEL graphs can be written.
PyHMDB is still under development and still lacks some aspects of HMDB. Please find more information about the current status of PyHMDB here_.

.. _here: current_status.html

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation_guide

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   models
   manager
   bel_serialization
   construct_namespaces

.. toctree::
   :maxdepth: 2
   :caption: How To

   set_up_hmdb

.. toctree::
   :maxdepth: 2
   :caption: Project

   current_status

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
