# -*- coding: utf-8 -*-

"""Work in progress.
- Import database models
- Write test_populate
"""

import unittest

import os
import tempfile

from bio2bel_hmdb.manager import Manager
from tests.constants import text_xml_path


class TestBuildDB(unittest.TestCase):
    def setUp(self):
        """Create temporary file"""

        self.fd, self.path = tempfile.mkstemp()
        self.connection = 'sqlite:///' + self.path

        # create temporary database
        self.manager = Manager(self.connection)
        # fill temporary database with test data
        self.manager.populate(text_xml_path)

    def tearDown(self):
        """Closes the connection in the manager and deletes the temporary database"""
        self.manager.session.close()
        os.close(self.fd)
        os.remove(self.path)

    def test_populate(self):
        """Test the populate function of the database manager"""
        pass


if __name__ == '__main__':
    unittest.main()
