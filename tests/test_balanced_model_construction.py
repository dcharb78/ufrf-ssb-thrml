import unittest
from collections import Counter

import numpy as np

from ufrf_ssb.hamiltonian import build_balanced_model


class TestBalancedModelConstruction(unittest.TestCase):
    def test_directed_edge_multiplicity_is_exactly_two(self):
        model, nodes, n, _ = build_balanced_model(14)
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        undirected = [
            tuple(sorted((node_to_idx[a], node_to_idx[b])))
            for a, b in model.edges
        ]
        counts = Counter(undirected)

        self.assertEqual(len(model.edges), 4 * n)
        self.assertEqual(len(counts), 2 * n)
        self.assertEqual(min(counts.values()), 2)
        self.assertEqual(max(counts.values()), 2)

    def test_all_weights_are_positive_in_default_balanced_regime(self):
        model, _, _, _ = build_balanced_model(14)
        weights = np.asarray(model.weights)
        self.assertTrue(np.all(weights > 0))


if __name__ == "__main__":
    unittest.main()
