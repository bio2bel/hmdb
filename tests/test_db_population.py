# -*- coding: utf-8 -*-

"""Work in progress.
- Import database models
- Write test_populate
"""

import unittest
import os
import tempfile

from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite, Biofluids, MetaboliteBiofluid, Synonyms, SecondaryAccessions
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


    def test_populate_metabolite(self):
        """Test the population of the metabolite table"""

        meta1 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00008").first()
        self.assertEqual("AFENDNXGAFYKQO-UHFFFAOYSA-N", meta1.inchikey)

        meta2 = self.manager.session.query(Metabolite).count()
        self.assertEqual(3, meta2)


    def test_populate_biofluid_locations(self):
        """Test the population of the biofluid and biofluid/metabolite mapping table"""

        # test if HMDB00064 has 7 associated biofluids
        metabio1 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00064").first()
        self.assertEqual(7, len(metabio1.biofluids))

        # test if there are 8 biofluids in total
        metabio2 = self.manager.session.query(Biofluids).count()
        self.assertEqual(8, metabio2)


    def test_populate_synonyms(self):
        """Test if the synonyms table is getting populated by the manager"""

        syn1 = self.manager.session.query(Synonyms).count()
        self.assertEqual(9, syn1)

        syn2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00072").first()
        self.assertEqual("(1Z)-1-Propene-1,2,3-tricarboxylate", syn2.synonyms[0].synonym)


    def test_populate_secondary_accessions(self):
        """Test if populate function populates the secondary accession table correctly"""
        seca1 = self.manager.session.query(SecondaryAccessions).count()
        self.assertEqual(1, seca1)

        seca2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00072").first()
        self.assertEqual("HMDB00461", seca2.secondary_accessions[0].secondary_accession)


if __name__ == '__main__':
    unittest.main()
