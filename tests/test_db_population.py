# -*- coding: utf-8 -*-

import os
import tempfile
import unittest
from collections import defaultdict

from bio2bel_hmdb.manager import Manager
from bio2bel_hmdb.models import Metabolite
from tests.constants import DatabaseMixin, text_xml_path


class TestBuildDB(DatabaseMixin):
    def test_populate_metabolite(self):
        """Test the population of the 'Metabolite' table"""
        meta1 = self.manager.get_metabolite_by_accession("HMDB00008")
        self.assertIsNotNone(meta1)
        self.assertEqual("AFENDNXGAFYKQO-UHFFFAOYSA-N", meta1.inchikey)

        meta2 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertIsNotNone(meta2)
        self.assertEqual("DB00148", meta2.drugbank_id)

    def test_populate_biofluid_locations(self):
        """Test the population of the 'Biofluids' and 'BiofluidMetabolite' relation table"""
        # test if HMDB00064 has 7 associated biofluids
        metabio1 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertIsNotNone(metabio1)
        self.assertIsInstance(metabio1, Metabolite)
        self.assertEqual(7, len(metabio1.biofluids))

        metabio1 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertIsNotNone(metabio1)
        self.assertEqual("Breast Milk", metabio1.biofluids[1].biofluid.biofluid)

    def test_populate_synonyms(self):
        """Test if the 'Synonyms' table is getting populated by the manager."""
        syn = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertEqual("(1Z)-1-Propene-1,2,3-tricarboxylate", syn.synonyms[0].synonym)

    def test_populate_secondary_accessions(self):
        """Test if the manager populate function populates the 'SecondaryAccessions' table correctly."""
        seca = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertIsNotNone(seca)
        self.assertEqual("HMDB00461", seca.accessions[0].secondary_accession)

    def test_populate_tissue_locations(self):
        """Test if the 'Tissues' table and 'MetaboliteTissues' table are populated by the manager"""
        tis = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertIsNotNone(tis)
        self.assertEqual(18, len(tis.tissues))
        # test the tissue of the tissue object connected to the metabolite object via the metabolitetissue object
        tis = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertIsNotNone(tis)
        self.assertEqual("Prostate", tis.tissues[-1].tissue.tissue)

    def test_populate_pathways(self):
        """Test for testing the population of the Pathways and MetabolitePathways tables"""
        pat2 = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertIsNotNone(pat2)
        self.assertEqual(15, len(pat2.pathways))

        pat3 = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertIsNotNone(pat3)
        self.assertEqual("SMP00549", pat3.pathways[0].pathway.smpdb_id)

    def test_populate_proteins(self):
        """Tests for testing if population of Protein and MetaboliteProtein table is successfull"""
        self.assertEqual(6, self.manager.count_proteins())

        pro = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertIsNotNone(pro)
        self.assertEqual(2, len(pro.proteins))

        pro = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertIsNotNone(pro)
        self.assertEqual("HMDBP00725", pro.proteins[0].protein.protein_accession)

    def test_populate_references(self):
        """Tests for testing if population of References and MetaboliteReferences table is successfull"""
        self.assertEqual(11, self.manager.count_references())

        ref = self.manager.get_reference_by_pubmed_id("7126379")
        self.assertIsNotNone(ref)
        self.assertEqual("Kobayash74.", ref.reference_text)

    def test_populate_diseases(self):
        """Tests for testing if population of Diseases and MetaboliteDiseases table is successfull"""
        self.assertEqual(3, self.manager.count_diseases())

    def test_populate_cellular_locations(self):
        """Tests for testing if population of CellularLocation and MetaboliteCelularLocations table is successfull"""
        self.assertEqual(3, self.manager.count_cellular_locations())

        cel2 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertIsNotNone(cel2)
        self.assertEqual("Mitochondria", cel2.cellular_locations[2].cellular_location.cellular_location)

    def test_populate_biofunctions(self):
        """Tests for testing if population of Biofunctions and MetaboliteBiofunctions table is successfull"""
        self.assertEqual(3, self.manager.count_biofunctions())

        biof2 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertIsNotNone(biof2)
        self.assertEqual("Component of Arginine and proline metabolism", biof2.biofunctions[0].biofunction.biofunction)


class TestDiseaseMapping(unittest.TestCase):
    """Tests for the disease name mapping"""

    def setUp(self):
        """Create temporary file"""

        self.fd, self.path = tempfile.mkstemp()
        self.connection = 'sqlite:///' + self.path

        # create temporary database
        self.manager = Manager(self.connection)
        self.manager.create_all()
        # fill temporary database with test data
        self.manager.populate(text_xml_path)

    def tearDown(self):
        """Closes the connection in the manager and deletes the temporary database"""
        self.manager.session.close()
        os.close(self.fd)
        os.remove(self.path)

    def test_disease_mapping(self):
        """test if diseases are mapped correctly"""
        metabolite = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertIsNotNone(metabolite)

        disease_references = metabolite.diseases

        dd = defaultdict(list)
        for disease_reference in disease_references:
            dd[disease_reference.disease.name].append(disease_reference)

        self.assertIn('Schizophrenia', dd)
        self.assertIn('Lung Cancer', dd)

        schz_entries = {
            entry.reference.pubmed_id: entry
            for entry in dd['Schizophrenia']
        }
        self.assertIn('2415198', schz_entries)

        for entry in schz_entries.values():
            self.assertIsNotNone(entry.disease)
            self.assertIsNotNone(entry.disease.hpo)
            self.assertEqual("Schizophrenia", entry.disease.hpo)

        lc_entries = {
            entry.reference.pubmed_id: entry
            for entry in dd['Lung Cancer']
        }

        for entry in lc_entries.values():
            self.assertEqual("lung cancer", entry.disease.dion)
