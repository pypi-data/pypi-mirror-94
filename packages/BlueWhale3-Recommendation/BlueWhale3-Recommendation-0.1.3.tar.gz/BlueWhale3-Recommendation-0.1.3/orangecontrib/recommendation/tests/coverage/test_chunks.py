import Orange
from orangecontrib.recommendation.utils.format_data import *
from orangecontrib.recommendation.utils.datacaching import *
from orangecontrib.recommendation.evaluation import ReciprocalRank

from scipy.sparse import *

import unittest
import numpy as np


class TestChunks(unittest.TestCase):

    def test_sparse_matrices(self):
        row = np.array([0, 0, 1, 2, 2, 2])
        col = np.array([0, 2, 2, 0, 1, 2])
        data = np.array([1, 2, 3, 4, 5, 6])
        shape = (3, 3)

        MATRIX_TYPES = [csc_matrix, csr_matrix, bsr_matrix, lil_matrix,
                        dok_matrix,  coo_matrix, dia_matrix]

        for mt in MATRIX_TYPES:
            sparse_matrix = sparse_matrix_2d(row, col, data, shape, mt)
            self.assertIsInstance(sparse_matrix, mt)

        mt = "Something to raise an error"
        self.assertRaises(Exception, lambda: sparse_matrix_2d(row, col, data,
                                                              shape, mt))

    def test_reciprocal_rank(self):
        results = np.array([[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]])
        query = np.array([[1], [5]])
        ranks = ReciprocalRank(results, query)

        self.assertEqual(len(ranks), len(query))

    def test_preprocess(self):
        # Test error
        param = "Something to raise an error"
        self.assertRaises(TypeError, lambda: preprocess(param))

        # Test heuristics
        iris = Orange.data.Table("iris.tab")
        preprocess(iris)

    def test_caches(self):
        row = np.array([0, 0, 1, 2, 2, 2])
        col = np.array([0, 2, 2, 0, 1, 2])
        data = np.array([1, 2, 3, 4, 5, 6])
        shape = (3, 3)
        m = sparse_matrix_2d(row, col, data, shape, csr_matrix)
        m2 = sparse_matrix_2d(row, col, data, shape, lil_matrix)

        self.assertEqual(0, len(cache_rows(m, 10, {1: [2]})))
        self.assertRaises(TypeError, lambda: cache_rows(m, 0, {1: [2]}))
        self.assertRaises(AttributeError, lambda: cache_rows(m2, 0, 0))
        self.assertRaises(Exception, lambda: cache_rows(m, 0, 0))

        indices = np.asarray([0, 1, 2])
        self.assertRaises(TypeError, lambda: cache_norms(m, indices, indices))
        self.assertRaises(TypeError, lambda: cache_norms(m, indices, "error"))

    def test_fix_predictions_rating(self):
        from orangecontrib.recommendation import BRISMFLearner

        data = Orange.data.Table('ratings.tab')
        learner = BRISMFLearner(num_factors=2, num_iter=1)
        recommender = learner(data)

        # Predict: {user, item} exists
        # Predict: Only user exists
        # Predict Only item exists
        # Predict: No one exists

        samples = np.array([[0, 0], [0, 1e5], [1e5, 0], [1e5, 1e5]])
        recommender(samples)

if __name__ == "__main__":
    # # Test all
    # unittest.main()

    # Test single test
    suite = unittest.TestSuite()
    suite.addTest(TestChunks("test_fix_predictions_rating"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
