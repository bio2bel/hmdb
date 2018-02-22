# -*- coding: utf-8 -*-

"""Bio2BEL HMDB is a package which allows the user to work with a local sqlite version of the Human Metabolome
Database (HMDB).

Next to creating the local database there are also functions provided, which will enrich given Biological Expression
Language (BEL) graphs with information about metabolites, proteins and diseases, that is present in HMDB.

HMDB BEL namespaces for these BEL graphs can be written.

Installation
------------
Get the Latest
~~~~~~~~~~~~~~~
Download the most recent code from `GitHub <https://github.com/bio2bel/hmdb>`_ with:

.. code-block:: sh

   $ python3 -m pip install git+https://github.com/bio2bel/hmdb.git

For Developers
~~~~~~~~~~~~~~
Clone the repository from `GitHub <https://github.com/bio2bel/hmdb>`_ and install in editable mode with:

.. code-block:: sh

   $ git clone https://github.com/bio2bel/hmdb.git
   $ cd hmdb
   $ python3 -m pip install -e .


Setup
-----
1. Create a :class:`bio2bel_hmdb.Manager` object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> from bio2bel_hmdb import Manager
>>> manager = Manager()

2. Create the tables in the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
>>> manager.create_all()

3. Populate the database
~~~~~~~~~~~~~~~~~~~~~~~~
This step will take sometime since the HMDB XML data needs to be downloaded, parsed, and fed into the database line
by line.

>>> manager.populate()
"""

from .manager import Manager

__version__ = '0.1.1-dev'

__title__ = 'bio2bel_hmdb'
__description__ = "A package for converting the Human Metabolome Database (HMDB) to BEL."
__url__ = 'https://github.com/bio2bel/hmdb'

__author__ = 'Charles Tapley Hoyt and Colin Birkenbihl'
__email__ = 'charles.hoyt@scai.fraunhofer.de'

__license__ = 'MIT License'
__copyright__ = 'Copyright (c) 2017-2018 Charles Tapley Hoyt and Colin Birkenbihl'
