Set up local HMDB version
=========================

Setting up a local version of the HMDB is eas using PyHMDB.

1. A Manager object needs to be created:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from PyHMDB.manager import Manager

> ``m = Manager()``

2. The Manager needs to create the datamodel/SQL tables:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

> ``m.make_tables()``

3. The database gets populated:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This step will take sometime, since the HMDB .xml data needs to be downloaded, parsed and fed into the database line by line.

> ``m.populate()``

The database should be up and running after this step and can be accessed using the Manager.session and SQLalchemy.
For more information about the database construction and querying the database please find the Manager_ documentation.

.. _Manager: manager.html




