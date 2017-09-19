# -*- coding: utf-8 -*-

"""Work in progress.
- Import database models
- Write test_populate
"""

import unittest
import os
import tempfile

from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite, Biofluids, MetaboliteBiofluid
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
        #test if HMDB00064 has 7 associated biofluids
        metabio1 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00064").first()
        self.assertEqual(7, len(metabio1.biofluid))

        #test if there are 8 biofluids in total
        metabio2 = self.manager.session.query(Biofluids).count()
        self.assertEqual(8, metabio2)


if __name__ == '__main__':
    unittest.main()
