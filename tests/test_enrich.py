# -*- coding: utf-8 -*-

from pybel import BELGraph

from bio2bel_hmdb.enrich import *
from tests.constants import DatabaseMixin

hmdb_tuple1 = ABUNDANCE, 'HMDB', 'HMDB00008'
protein_tuple = PROTEIN, 'UP', 'P50440'

# test enriching with tissues
hmdb_tuple2 = ABUNDANCE, 'HMDB', 'HMDB00064'
disease_tuple = PATHOLOGY, 'HMDB_D', 'Lung Cancer'


class TestEnrich(DatabaseMixin):
    def test_enrich_metabolites_proteins(self):
        g = BELGraph()
        g.add_simple_node(*hmdb_tuple1)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_metabolites_proteins(g)
        self.assertEqual(4, g.number_of_nodes())
        self.assertEqual(3, g.number_of_edges())
        self.assertTrue(g.has_edge(protein_tuple, hmdb_tuple1))

    def test_enrich_metabolites_diseases(self):
        g = BELGraph()
        g.add_simple_node(*hmdb_tuple2)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_metabolites_diseases(g)
        self.assertEqual(4, g.number_of_nodes())
        self.assertEqual(3, g.number_of_edges())
        self.assertTrue(g.has_edge(disease_tuple, hmdb_tuple2))

    def test_enrich_diseases_metabolites(self):
        g = BELGraph()
        g.add_simple_node(*disease_tuple)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_diseases_metabolites(g)
        self.assertEqual(3, g.number_of_nodes())
        self.assertEqual(2, g.number_of_edges())
        self.assertTrue(g.has_edge(hmdb_tuple2, disease_tuple))

    def test_enrich_proteins_metabolites(self):
        g = BELGraph()
        g.add_simple_node(*protein_tuple)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_proteins_metabolites(g)
        self.assertEqual(3, g.number_of_nodes())
        self.assertEqual(2, g.number_of_edges())
        self.assertTrue(g.has_edge(hmdb_tuple1, protein_tuple))
