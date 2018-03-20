# -*- coding: utf-8 -*-

from bio2bel_hmdb.constants import DOID, HP
from bio2bel_hmdb.to_belns import construct_hmdb_disease_mapping
from tests.constants import DatabaseMixin

diseases = ['Cirrhosis', 'Lung Cancer', 'Schizophrenia']


class TestCreateNS(DatabaseMixin):
    def test_get_hmdb_accessions(self):
        hmdb_accession = self.manager.get_hmdb_accession()
        self.assertEqual(['HMDB00008', 'HMDB00064', 'HMDB00072'], hmdb_accession)

    def test_get_hmdb_diseases(self):
        """Test that :meth:`bio2bel_hmdb.Manager.get_hmdb_diseases` extracts all HMDB accessions from the database"""
        hmdb_diseases = self.manager.get_hmdb_diseases()
        self.assertEqual(diseases, hmdb_diseases)

    def test_create_disease_mapping(self):
        """Test for the maping function that maps HMDB disease names to different ontologies"""
        mapping, length = construct_hmdb_disease_mapping(self.manager)
        self.assertEqual(0, length)
        keys = list(mapping[HP].keys()) + list(mapping[DOID].keys())
        values = list(mapping[HP].values()) + list(mapping[DOID].values())
        self.assertEqual(set(diseases), set(keys))
        self.assertEqual({'Cirrhosis', 'lung cancer', 'schizophrenia'}, set(values))
