# -*- coding: utf-8 -*-

"""Work in progress.
- Import database models
- Write test_populate
"""

import unittest
import os
import tempfile

from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite, Biofluids, Synonyms, \
    SecondaryAccessions, Tissues, Pathways, Proteins
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

    def test_populate_tissue_locations(self):
        """Test if the tissues and metabolite tissues table are populated by the manager"""

        tis1 = self.manager.session.query(Tissues).count()
        self.assertEqual(3, tis1)
        # test the tissue of the tissue object connected to the metabolite object via the metabolitetissue object
        tis2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00064").first()
        self.assertEqual("Adipose Tissue", tis2.tissues[0].tissue.tissue)

    def test_populate_pathways(self):
        """Test for testing the population of the Pathways and MetabolitePathways tables"""
        pat1 = self.manager.session.query(Pathways).count()
        self.assertEqual(4, pat1)

        pat2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == 'HMDB00072').first()
        self.assertEqual(3, len(pat2.pathways))

        pat3 = self.manager.session.query(Metabolite).filter(Metabolite.accession == 'HMDB00072').first()
        self.assertEqual("double test added by colin", pat3.pathways[1].pathway.name)

    def test_populate_proteins(self):
        """Tests for testing if population of Protein and MetaboliteProtein table is successfull"""
        pro1 = self.manager.session.query(Proteins).count()
        self.assertEqual(6, pro1)

        pro2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == 'HMDB00072').first()
        self.assertEqual(2, len(pro2.proteins))

        pro3 = self.manager.session.query(Metabolite).filter(Metabolite.accession == 'HMDB00072').first()
        self.assertEqual("HMDBP00725", pro3.proteins[1].protein.protein_accession)


if __name__ == '__main__':
    unittest.main()
