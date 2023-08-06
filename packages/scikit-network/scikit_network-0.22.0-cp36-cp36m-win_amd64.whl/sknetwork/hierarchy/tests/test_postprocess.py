#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 2019
@author: Thomas Bonald <bonald@enst.fr>
@author: Quentin Lutz <qlutz@enst.fr>
"""

import unittest

from sknetwork.data import karate_club
from sknetwork.hierarchy import Paris, cut_straight, cut_balanced, aggregate_dendrogram


# noinspection PyMissingOrEmptyDocstring
class TestCuts(unittest.TestCase):

    def setUp(self):
        paris = Paris()
        adjacency = karate_club()
        self.dendrogram = paris.fit_transform(adjacency)

    def test_cuts(self):
        labels = cut_straight(self.dendrogram)
        self.assertEqual(len(set(labels)), 2)
        labels = cut_straight(self.dendrogram, n_clusters=5)
        self.assertEqual(len(set(labels)), 5)
        labels = cut_balanced(self.dendrogram, 2)
        self.assertEqual(len(set(labels)), 21)
        labels, new_dendrogram = cut_balanced(self.dendrogram, max_cluster_size=2, return_dendrogram=True)
        self.assertEqual(len(set(labels)), 21)
        self.assertTupleEqual(new_dendrogram.shape, (20, 4))

    def test_options(self):
        labels = cut_straight(self.dendrogram, threshold=0.5)
        self.assertEqual(len(set(labels)), 4)
        labels = cut_straight(self.dendrogram, n_clusters=3, threshold=0.5)
        self.assertEqual(len(set(labels)), 3)
        labels = cut_straight(self.dendrogram, sort_clusters=False)
        self.assertEqual(len(set(labels)), 2)
        labels = cut_balanced(self.dendrogram, max_cluster_size=2, sort_clusters=False)
        self.assertEqual(len(set(labels)), 21)
        labels = cut_balanced(self.dendrogram, max_cluster_size=10)
        self.assertEqual(len(set(labels)), 5)

    def test_aggregation(self):
        aggregated = aggregate_dendrogram(self.dendrogram, n_clusters=3)
        self.assertEqual(len(aggregated), 2)

        aggregated, counts = aggregate_dendrogram(self.dendrogram, n_clusters=3, return_counts=True)
        self.assertEqual(len(aggregated), 2)
        self.assertEqual(len(counts), 3)

