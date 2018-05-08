Bio2BEL HMDB |build| |coverage| |documentation|
===============================================
Converts the Human Metabolite Database (HMDB) to BEL

Installation |pypi_version| |python_versions| |pypi_license|
------------------------------------------------------------
``bio2bel_hmdb`` can be installed easily from `PyPI <https://pypi.python.org/pypi/bio2bel_hmdb>`_ with
the following code in your favorite terminal:

.. code-block:: sh

    $ python3 -m pip install bio2bel_hmdb

or from the latest code on `GitHub <https://github.com/bio2bel/hmdb>`_ with:

.. code-block:: sh

    $ python3 -m pip install git+https://github.com/bio2bel/hmdb.git@master

Setup
-----
HMDB can be downloaded and populated from either the Python REPL or the automatically installed command line
utility.

Python REPL
~~~~~~~~~~~
.. code-block:: python

    >>> import bio2bel_hmdb
    >>> hmdb_manager = bio2bel_hmdb.Manager()
    >>> hmdb_manager.populate()

Command Line Utility
~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    bio2bel_hmdb populate

Citations
---------
- Wishart DS, *et al.*, HMDB: the Human Metabolome Database. Nucleic Acids Res. 2007 Jan;35(Database issue):D521-6

.. |build| image:: https://travis-ci.org/bio2bel/hmdb.svg?branch=master
    :target: https://travis-ci.org/bio2bel/hmdb
    :alt: Build Status

.. |documentation| image:: http://readthedocs.org/projects/bio2bel-hmdb/badge/?version=latest
    :target: http://bio2bel.readthedocs.io/projects/hmdb/en/latest/?badge=latest
    :alt: Documentation Status

.. |pypi_version| image:: https://img.shields.io/pypi/v/bio2bel_hmdb.svg
    :alt: Current version on PyPI

.. |coverage| image:: https://codecov.io/gh/bio2bel/hmdb/coverage.svg?branch=master
    :target: https://codecov.io/gh/bio2bel/hmdb?branch=master
    :alt: Coverage Status

.. |climate| image:: https://codeclimate.com/github/bio2bel/hmdb/badges/gpa.svg
    :target: https://codeclimate.com/github/bio2bel/hmdb
    :alt: Code Climate

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/bio2bel_hmdb.svg
    :alt: Stable Supported Python Versions

.. |pypi_license| image:: https://img.shields.io/pypi/l/bio2bel_hmdb.svg
    :alt: MIT License
