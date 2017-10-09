# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

from bio2bel_hmdb.manager import Manager
from tests.constants import text_xml_path


class TestWriteBelDocument(unittest.TestCase):
    """Tests for the disease name mapping"""

    def setUp(self):
        """Create temporary file"""

        self.fd, self.path = tempfile.mkstemp()
        self.connection = 'sqlite:///' + self.path

        # create temporary database
        self.manager = Manager(self.connection)
        self.manager.make_tables()
        # fill temporary database with test data
        self.manager.populate(text_xml_path)

    def tearDown(self):
        """Closes the connection in the manager and deletes the temporary database"""
        self.manager.session.close()
        os.close(self.fd)
        os.remove(self.path)

    def test_write_bel_asso(self):
        """test if diseases are mapped correctly"""

    raise NotImplementedError
