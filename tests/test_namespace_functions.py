# -*- coding: utf-8 -*-

import unittest

from tests.constants import DatabaseMixin

class TestBuildDB(DatabaseMixin):
    def test_write_hmdb_ns(self):
        raise NotImplementedError

    def test_map_to_ontologies(self):
        raise NotImplementedError

    def test_get_hmdb_accessions(self):
        raise NotImplementedError

    def test_get_hmdb_diseases(self):
        raise NotImplementedError

