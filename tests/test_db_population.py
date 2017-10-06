# -*- coding: utf-8 -*-

import unittest

from bio2bel_hmdb.models import Metabolite, Proteins, References, Diseases, CellularLocations, Biofunctions
from tests.constants import DatabaseMixin


class TestBuildDB(DatabaseMixin):
    def test_populate_metabolite(self):
        """Test the population of the 'Metabolite' table"""

        meta1 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00008").one_or_none()
        self.assertEqual("AFENDNXGAFYKQO-UHFFFAOYSA-N", meta1.inchikey)

        meta2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00064").one_or_none()
        self.assertEqual("DB00148", meta2.drugbank_id)

    def test_populate_biofluid_locations(self):
        """Test the population of the 'Biofluids' and 'BiofluidMetabolite' relation table"""

        # test if HMDB00064 has 7 associated biofluids
        metabio1 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertEqual(7, len(metabio1.biofluids))

        metabio1 = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertEqual("Breast Milk", metabio1.biofluids[1].biofluid.biofluid)

    def test_populate_synonyms(self):
        """Test if the 'Synonyms' table is getting populated by the manager"""

        syn = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertEqual("(1Z)-1-Propene-1,2,3-tricarboxylate", syn.synonyms[0].synonym)

    def test_populate_secondary_accessions(self):
        """Test if the manager populate function populates the 'SecondaryAccessions' table correctly"""
        seca = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertEqual("HMDB00461", seca.secondary_accessions[0].secondary_accession)

    def test_populate_tissue_locations(self):
        """Test if the 'Tissues' table and 'MetaboliteTissues' table are populated by the manager"""
        tis = self.manager.get_metabolite_by_accession("HMDB00064")
        self.assertEqual(18, len(tis.tissues))
        # test the tissue of the tissue object connected to the metabolite object via the metabolitetissue object
        tis = self.manager.get_metabolite_by_accession("HMDB00072")
        self.assertEqual("Prostate", tis.tissues[-1].tissue.tissue)

    def test_populate_pathways(self):
        """Test for testing the population of the Pathways and MetabolitePathways tables"""

        pat2 = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertEqual(15, len(pat2.pathways))

        pat3 = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertEqual("SMP00549", pat3.pathways[0].pathway.smpdb_id)

    def test_populate_proteins(self):
        """Tests for testing if population of Protein and MetaboliteProtein table is successfull"""
        pro1 = self.manager.session.query(Proteins).count()
        self.assertEqual(6, pro1)

        pro2 = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertEqual(2, len(pro2.proteins))

        pro3 = self.manager.get_metabolite_by_accession('HMDB00072')
        self.assertEqual("HMDBP00725", pro3.proteins[0].protein.protein_accession)

    def test_populate_references(self):
        """Tests for testing if population of References and MetaboliteReferences table is successfull"""
        ref1 = self.manager.session.query(References).count()
        self.assertEqual(11, ref1)

        ref2 = self.manager.session.query(References).filter(References.pubmed_id == "7126379")
        self.assertEqual("Kobayash74.", ref2[0].reference_text)

    def test_populate_diseases(self):
        """Tests for testing if population of Diseases and MetaboliteDiseases table is successfull"""
        dis = self.manager.session.query(Diseases).count()
        self.assertEqual(3, dis)

        dis = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00072").first()
        self.assertEqual("Schizophrenia", dis.diseases[1].disease.name)
        self.assertEqual("2415198", dis.diseases[1].reference.pubmed_id)
        # test mapping
        self.assertEqual("lung cancer", dis.diseases[2].disease.dion)
        self.assertEqual("Schizophrenia", dis.diseases[1].disease.hpo)

    def test_populate_cellular_locations(self):
        """Tests for testing if population of CellularLocation and MetaboliteCelularLocations table is successfull"""
        cel1 = self.manager.session.query(CellularLocations).count()
        self.assertEqual(3, cel1)

        cel2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00064")
        self.assertEqual("Mitochondria", cel2[0].cellular_locations[2].cellular_location.cellular_location)

    def test_populate_biofunctions(self):
        """Tests for testing if population of Biofunctions and MetaboliteBiofunctions table is successfull"""
        biof1 = self.manager.session.query(Biofunctions).count()
        self.assertEqual(3, biof1)

        biof2 = self.manager.session.query(Metabolite).filter(Metabolite.accession == "HMDB00064")
        self.assertEqual("Component of Arginine and proline metabolism",
                         biof2[0].biofunctions[0].biofunction.biofunction)


if __name__ == '__main__':
    unittest.main()
