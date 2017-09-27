# -*- coding: utf-8 -*-

import unittest

from pybel import BELGraph
from pybel.constants import PROTEIN, ABUNDANCE
from bio2bel_hmdb.enrich import *

hmdb_tuple1 = ABUNDANCE, 'HMDB', 'HMDB00008'
protein = PROTEIN, 'UP', 'P50440'

# test enriching with tissues
hmdb_tuple2 = ABUNDANCE, 'HMDB', 'HMDB00064'
disease = PATHOLOGY, 'HMDB_D', 'Lung Cancer'


class TestEnrich(unittest.TestCase):
    def test_enrich_proteins(self):
        g = BELGraph()
        g.add_simple_node(*hmdb_tuple1)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_metabolites_proteins(g)
        self.assertEqual(4, g.number_of_nodes())
        self.assertEqual(3, g.number_of_edges())
        self.assertTrue(g.has_edge(protein, hmdb_tuple1))

    def test_enrich_diseases(self):
        g = BELGraph()
        g.add_simple_node(*hmdb_tuple2)

        self.assertEqual(1, g.number_of_nodes())
        self.assertEqual(0, g.number_of_edges())

        enrich_metabolites_diseases(g)
        self.assertEqual(4, g.number_of_nodes())
        self.assertEqual(3, g.number_of_edges())
        self.assertTrue(g.has_edge(disease, hmdb_tuple2))
