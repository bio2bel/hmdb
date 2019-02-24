# -*- coding: utf-8 -*-

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
