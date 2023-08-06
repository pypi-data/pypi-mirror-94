#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for polynomes"""

import unittest

import numpy as np
from scipy import sparse

from sknetwork.data.test_graphs import test_graph
from sknetwork.linalg import Polynome, randomized_eig, randomized_svd


class TestPolynome(unittest.TestCase):

    def test_init(self):
        adjacency = test_graph()
        with self.assertRaises(ValueError):
            Polynome(adjacency, np.array([]))

    def test_operations(self):
        adjacency = test_graph()
        n = adjacency.shape[0]
        polynome = Polynome(adjacency, np.arange(3))
        x = np.random.randn(n)

        y1 = (polynome * 2).dot(x)
        y2 = (-polynome).dot(x)
        self.assertAlmostEqual(np.linalg.norm(0.5 * y1 + y2), 0)

    def test_dot(self):
        adjacency = sparse.eye(5, format='csr')
        polynome = Polynome(adjacency, np.arange(2))

        x = np.random.randn(5, 3)
        y = polynome.dot(x)
        self.assertAlmostEqual(np.linalg.norm(x - y), 0)

    def test_decomposition(self):
        adjacency = test_graph()
        n = adjacency.shape[0]
        polynome = Polynome(adjacency, np.arange(3))

        eigenvalues, eigenvectors = randomized_eig(polynome, n_components=2, which='LM')
        self.assertEqual(eigenvalues.shape, (2,))
        self.assertEqual(eigenvectors.shape, (n, 2))

        left_sv, sv, right_sv = randomized_svd(polynome, n_components=2)
        self.assertEqual(left_sv.shape, (n, 2))
        self.assertEqual(sv.shape, (2,))
        self.assertEqual(right_sv.shape, (2, n))
