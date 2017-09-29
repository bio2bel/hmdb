# -*- coding: utf-8 -*-

import unittest

import os
import tempfile

from bio2bel_hmdb.manager import Manager

dir_path = os.path.dirname(os.path.realpath(__file__))

text_xml_path = os.path.join(dir_path, 'test_data.xml')


class DatabaseMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary file"""

        cls.fd, cls.path = tempfile.mkstemp()
        cls.connection = 'sqlite:///' + cls.path

        # create temporary database
        cls.manager = Manager(cls.connection)
        cls.manager.make_tables()
        # fill temporary database with test data
        cls.manager.populate(text_xml_path)

    @classmethod
    def tearDownClass(cls):
        """Closes the connection in the manager and deletes the temporary database"""
        cls.manager.session.close()
        os.close(cls.fd)
        os.remove(cls.path)
