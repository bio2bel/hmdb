# -*- coding: utf-8 -*-

from bio2bel_hmdb.enrich import *
from pybel import BELGraph
from pybel.dsl import Abundance, Pathology, Protein
from tests.constants import DatabaseMixin

hmdb_tuple1 = Abundance('HMDB', 'HMDB00008')
protein_tuple = Protein('UP', 'P50440')

# test enriching with tissues
hmdb_tuple2 = Abundance('HMDB', 'HMDB00064')
disease_tuple = Pathology('HMDB_D', 'Lung Cancer')


class TestEnrich(DatabaseMixin):
    def test_enrich_metabolites_proteins(self):
        g = BELGraph()
        g.add_node_from_data(hmdb_tuple1)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_metabolites_proteins(g, self.manager)
        self.assertEqual(4, g.number_of_nodes())
        self.assertEqual(3, g.number_of_edges())
        self.assertTrue(g.has_edge(protein_tuple, hmdb_tuple1))

    def test_enrich_metabolites_diseases(self):
        g = BELGraph()
        g.add_node_from_data(hmdb_tuple2)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_metabolites_diseases(g, self.manager)
        self.assertEqual(4, g.number_of_nodes())
        self.assertEqual(3, g.number_of_edges())
        self.assertTrue(g.has_edge(disease_tuple, hmdb_tuple2))

    def test_enrich_diseases_metabolites(self):
        g = BELGraph()
        g.add_node_from_data(disease_tuple)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_diseases_metabolites(g, self.manager)
        self.assertEqual(3, g.number_of_nodes())
        self.assertEqual(2, g.number_of_edges())
        self.assertTrue(g.has_edge(hmdb_tuple2, disease_tuple))

    def test_enrich_proteins_metabolites(self):
        g = BELGraph()
        g.add_node_from_data(protein_tuple)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_proteins_metabolites(g, self.manager)
        self.assertEqual(3, g.number_of_nodes())
        self.assertEqual(2, g.number_of_edges())
        self.assertTrue(g.has_edge(hmdb_tuple1, protein_tuple))
