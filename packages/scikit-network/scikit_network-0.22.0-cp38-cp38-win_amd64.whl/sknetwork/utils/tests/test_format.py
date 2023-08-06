#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for format.py"""
import unittest

from sknetwork.data import star_wars, house, cyclic_digraph
from sknetwork.utils.check import is_symmetric
from sknetwork.utils.format import *


class TestFormats(unittest.TestCase):

    def setUp(self):
        """Basic biadjacency for tests."""
        self.biadjacency = star_wars()

    def test_dir2undir(self):
        n = 3
        adjacency = cyclic_digraph(n)
        ref = directed2undirected(adjacency)
        self.assertEqual(ref.shape, adjacency.shape)
        self.assertTrue(is_symmetric(ref))

        adjacency = house()
        n = adjacency.shape[0]
        error = directed2undirected(adjacency, weighted=False) - adjacency
        self.assertEqual(error.nnz, 0)

        slr = SparseLR(adjacency, [(np.zeros(n), np.zeros(n))])
        self.assertRaises(ValueError, directed2undirected, slr, weighted=False)
        slr = 0.5 * directed2undirected(slr)
        self.assertEqual(slr.shape, (n, n))

        x = np.random.randn(n)
        error = np.linalg.norm(slr.dot(x) - adjacency.dot(x))
        self.assertAlmostEqual(error, 0)

    def test_bip2dir(self):
        n_row, n_col = self.biadjacency.shape
        n = n_row + n_col

        directed_graph = bipartite2directed(self.biadjacency)
        self.assertEqual(directed_graph.shape, (n, n))

        slr = SparseLR(self.biadjacency, [(np.ones(n_row), np.ones(n_col))])
        directed_graph = bipartite2directed(slr)
        self.assertTrue(type(directed_graph) == SparseLR)

    def test_bip2undir(self):
        n_row, n_col = self.biadjacency.shape
        n = n_row + n_col

        undirected_graph = bipartite2undirected(self.biadjacency)
        self.assertEqual(undirected_graph.shape, (n, n))
        self.assertTrue(is_symmetric(undirected_graph))

        slr = SparseLR(self.biadjacency, [(np.ones(n_row), np.ones(n_col))])
        undirected_graph = bipartite2undirected(slr)
        self.assertTrue(type(undirected_graph) == SparseLR)
