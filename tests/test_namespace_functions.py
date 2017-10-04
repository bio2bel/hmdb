# -*- coding: utf-8 -*-

import unittest

from tests.constants import DatabaseMixin
from bio2bel_hmdb.create_namespace import construct_hmdb_disease_mapping

diseases = ['Cirrhosis', 'Lung Cancer', 'Schizophrenia']


class TestCreateNS(DatabaseMixin):
    def test_get_hmdb_accessions(self):
        hmdb_accession = self.manager.get_hmdb_accession()
        self.assertEqual(['HMDB00008', 'HMDB00064', 'HMDB00072'], hmdb_accession)

    def test_get_hmdb_diseases(self):
        """Test for the get_hmdb_diseases function of the manager, that extracts all HMDB accessions from the database"""
        hmdb_diseases = self.manager.get_hmdb_diseases()
        self.assertEqual(diseases, hmdb_diseases)

    def test_create_disease_mapping(self):
        """Test for the maping function that maps HMDB disease names to different ontologies"""
        mapping, length = construct_hmdb_disease_mapping(self.manager)
        self.assertEqual(0, length)
        keys = list(mapping['human-phenotype-ontology'].keys()) + list(mapping['disease-ontology'].keys())
        values = list(mapping['human-phenotype-ontology'].values()) + list(mapping['disease-ontology'].values())
        self.assertEqual(set(diseases), set(keys))
        self.assertEqual({'Cirrhosis', 'lung cancer', 'schizophrenia'}, set(values))
