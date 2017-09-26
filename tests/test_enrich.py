# -*- coding: utf-8 -*-

import unittest

from pybel import BELGraph
from pybel.constants import PROTEIN, ABUNDANCE

from bio2bel_hmdb.enrich import *

hmdb8_tuple = ABUNDANCE, 'HMDB', 'HMDB00008'
t1 = PROTEIN, 'UP', 'P09622'


class TestEnrich(unittest.TestCase):
    def test_enrich(self):
        g = BELGraph()

        g.add_simple_node(*hmdb8_tuple)

        self.assertEqual(1, g.number_of_nodes())

        enrich_metabolites(g)
        self.assertEqual(3, g.number_of_nodes())
        self.assertEqual(2, g.number_of_edges())
        self.assertTrue(g.has_edge(t1, hmdb8_tuple))
