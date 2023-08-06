#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests for check.py"""
import unittest

from sknetwork.data import cyclic_digraph
from sknetwork.data.test_graphs import test_graph_disconnect
from sknetwork.utils.check import *
from sknetwork.utils.format import check_csr_or_slr


class TestChecks(unittest.TestCase):

    def setUp(self):
        """Simple graphs for tests."""
        self.adjacency = cyclic_digraph(3)
        self.dense_mat = np.identity(3)

    def test_check_format(self):
        with self.assertRaises(TypeError):
            check_format(self.adjacency.tocsc())

    def test_check_csr_slr(self):
        with self.assertRaises(TypeError):
            check_csr_or_slr(np.ones(3))

    def test_check_square(self):
        with self.assertRaises(ValueError):
            check_square(np.ones((3, 7)))

    def test_check_connected(self):
        with self.assertRaises(ValueError):
            check_connected(test_graph_disconnect())

    def test_check_symmetry(self):
        with self.assertRaises(ValueError):
            check_symmetry(self.adjacency)

    def test_nonnegative_entries(self):
        self.assertTrue(has_nonnegative_entries(self.adjacency))
        self.assertTrue(has_nonnegative_entries(self.dense_mat))

    def test_check_nonnegative(self):
        with self.assertRaises(ValueError):
            check_nonnegative(-self.dense_mat)

    def test_positive_entries(self):
        self.assertFalse(has_positive_entries(self.dense_mat))
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            has_positive_entries(self.adjacency)

    def test_check_positive(self):
        check_positive(np.ones(3))
        with self.assertRaises(ValueError):
            check_positive(-self.dense_mat)

    def test_probas(self):
        self.assertTrue(is_proba_array(np.array([.5, .5])))
        check_is_proba(0.5)
        with self.assertRaises(TypeError):
            is_proba_array(np.ones((2, 2, 2)))
        self.assertRaises(TypeError, check_is_proba, 'toto')
        with self.assertRaises(ValueError):
            check_is_proba(2)

    def test_damping(self):
        with self.assertRaises(ValueError):
            check_damping_factor(1)

    def test_error_make_weights(self):
        with self.assertRaises(ValueError):
            make_weights(distribution='junk', adjacency=self.adjacency)

    def test_error_check_is_proba(self):
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            check_is_proba('junk')
        with self.assertRaises(ValueError):
            check_is_proba(2)

    def test_error_check_weights(self):
        with self.assertRaises(ValueError):
            check_weights(np.zeros(4), self.adjacency)
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            check_weights(2, self.adjacency)
        with self.assertRaises(ValueError):
            check_weights(np.zeros(3), self.adjacency, positive_entries=True)
        with self.assertRaises(ValueError):
            check_weights(-np.ones(3), self.adjacency)

    def test_random_state(self):
        random_state = np.random.RandomState(1)
        self.assertEqual(type(check_random_state(random_state)), np.random.RandomState)

    def test_error_random_state(self):
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            check_random_state('junk')

    def test_check_seeds(self):
        n = 10
        seeds_array = -np.ones(n)
        seeds_array[:2] = np.arange(2)
        seeds_dict = {0: 0, 1: 1}
        labels_array = check_seeds(seeds_array, n)
        labels_dict = check_seeds(seeds_dict, n)

        self.assertTrue(np.allclose(labels_array, labels_dict))
        with self.assertRaises(ValueError):
            check_seeds(labels_array, 5)
        self.assertRaises(TypeError, check_seeds, 'toto', 3)
        with self.assertWarns(Warning):
            seeds_dict[0] = -1
            check_seeds(seeds_dict, n)

    def test_check_labels(self):
        with self.assertRaises(ValueError):
            check_labels(np.ones(3))
        labels = np.ones(5)
        labels[0] = 0
        classes, n_classes = check_labels(labels)
        self.assertTrue(np.equal(classes, np.arange(2)).all())
        self.assertEqual(n_classes, 2)

    def test_check_n_jobs(self):
        self.assertEqual(check_n_jobs(None), 1)
        self.assertEqual(check_n_jobs(-1), None)
        self.assertEqual(check_n_jobs(8), 8)

    def test_check_n_neighbors(self):
        with self.assertWarns(Warning):
            check_n_neighbors(10, 5)

    def test_adj_vector(self):
        n = 10
        vector1 = np.random.rand(n)
        vector2 = sparse.csr_matrix(vector1)
        adj1 = check_adjacency_vector(vector1)
        adj2 = check_adjacency_vector(vector2)

        self.assertEqual((adj1 - adj2).nnz, 0)
        self.assertEqual(adj1.shape, (1, n))

        with self.assertRaises(ValueError):
            check_adjacency_vector(vector1, 2 * n)

    def test_check_n_clusters(self):
        with self.assertRaises(ValueError):
            check_n_clusters(3, 2)
        with self.assertRaises(ValueError):
            check_n_clusters(0, 2, 1)

    def test_min_size(self):
        with self.assertRaises(ValueError):
            check_min_size(1, 3)

    def test_min_nnz(self):
        with self.assertRaises(ValueError):
            check_min_nnz(1, 3)

    def test_dendrogram(self):
        with self.assertRaises(ValueError):
            check_dendrogram(np.ones((3, 3)))

    def test_n_components(self):
        self.assertEqual(5, check_n_components(5, 10))
        with self.assertWarns(Warning):
            self.assertEqual(2, check_n_components(5, 2))

    def test_scaling(self):
        adjacency = cyclic_digraph(3)
        with self.assertRaises(ValueError):
            check_scaling(-1, adjacency, regularize=True)
