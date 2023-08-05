import Orange
from orangecontrib.recommendation.utils.format_data import *

from sklearn.metrics import mean_squared_error

import unittest
import numpy as np
import math
import random

__all__ = ['TestRatingModels', 'TestRankingModels']


class TestRatingModels:

    # @classmethod
    # def setUpClass(cls):
    #     if cls is TestRatingModels:
    #         raise unittest.SkipTest("Skip BaseTest tests, it's a base class")
    #     super(TestRatingModels, cls).setUpClass()

    def test_input_data_continuous(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender
        recommender = learner(data)

        print(str(recommender) + ' trained')

        # Compute predictions
        y_pred = recommender(data)

        # Compute RMSE
        rmse = math.sqrt(mean_squared_error(data.Y, y_pred))
        print('-> RMSE (input data; continuous): %.3f' % rmse)

        # Check correctness
        self.assertGreaterEqual(rmse, 0)

    def test_input_data_discrete(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender
        recommender = learner(data)
        print(str(recommender) + ' trained')

        # Compute predictions
        y_pred = recommender(data)

        # Compute RMSE
        rmse = math.sqrt(mean_squared_error(data.Y, y_pred))
        print('-> RMSE (input data; discrete): %.3f' % rmse)

        # Check correctness
        self.assertGreaterEqual(rmse, 0)

    def test_pairs(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender
        recommender = learner(data)

        # Create indices to test
        sample_size = 10
        num_users, num_items = recommender.shape
        idx_users = np.random.randint(0, num_users, size=sample_size)
        idx_items = np.random.randint(0, num_items, size=sample_size)
        indices = np.column_stack((idx_users, idx_items))

        # Compute predictions
        y_pred = recommender(indices)
        print('-> Same number? (pairs): %r' % (len(y_pred) == sample_size))

        # Check correctness
        self.assertEqual(len(y_pred), sample_size)

    def test_predict_items(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender
        recommender = learner(data)

        # Compute predictions 1
        prediction = recommender.predict_items(users=None, top=None)

        # Compute predictions 2 (Execute the other branch)
        num_users = min(recommender.shape[0], 5)
        num_items = min(recommender.shape[1], 5)
        setUsers = random.sample(range(recommender.shape[0]), num_users)
        prediction2 = recommender.predict_items(users=setUsers, top=num_items)

        # Check correctness 1
        len_u, len_i = prediction.shape
        self.assertEqual(len_u, recommender.shape[0])
        self.assertEqual(len_i, recommender.shape[1])

        # Check correctness 2
        len_u, len_i = prediction2.shape
        self.assertEqual(len_u, num_users)
        self.assertEqual(len_i, num_items)

    def test_CV(self, learner, filename):
        from Orange.evaluation.testing import CrossValidation

        # Load data
        data = Orange.data.Table(filename)

        learners = [learner]

        res = CrossValidation(data, learners, k=3)
        rmse = Orange.evaluation.RMSE(res)
        r2 = Orange.evaluation.R2(res)

        print("Learner  RMSE  R2")
        for i in range(len(learners)):
            print(
                "{:8s} {:.2f} {:5.2f}".format(learners[i].name, rmse[i], r2[i]))

        self.assertIsInstance(rmse, np.ndarray)

    def test_warnings(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender and check warns
        self.assertWarns(UserWarning, learner, data)

    def test_divergence(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender and check divergence
        self.assertRaises(RuntimeError, lambda: learner(data))

    def test_swap_columns(self, learner, filename1, filename2):
        # Load data
        data1 = Orange.data.Table(filename1)
        data2 = Orange.data.Table(filename2)

        # Train recommender
        recommender1 = learner(data1)
        recommender2 = learner(data2)

        # Compute predictions
        y_pred1 = recommender1(data1)
        y_pred2 = recommender2(data2)

        np.testing.assert_array_equal(y_pred1, y_pred2)

class TestRankingModels:

    # @classmethod
    # def setUpClass(cls):
    #     if cls is TestRankingModels:
    #         raise unittest.SkipTest("Skip BaseTest tests, it's a base class")
    #     super(TestRankingModels, cls).setUpClass()

    def test_input_data_continuous(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        recommender = learner(data)
        print(str(recommender) + ' trained')

        # Create set to test
        num_users = min(recommender.shape[0], 5)
        num_items = recommender.shape[1]
        test_users = random.sample(range(recommender.shape[0]), num_users)

        # Compute predictions 1
        y_pred = recommender(data[test_users], top_k=None)

        # Compute predictions 2 (Execute the 2nd branch)
        y_pred2 = recommender(data[test_users].X, top_k=num_items)

        # Compute predictions 3 (Execute the 3rd branch, "no arg")
        y_pred3 = recommender(data[test_users], no_real_arg='Something')

        # Compute predictions 4 (Check single user)
        y_pred4 = recommender(X=0, top_k=num_items)

        np.testing.assert_equal(y_pred, y_pred2)
        np.testing.assert_equal(y_pred, y_pred3)
        np.testing.assert_equal(y_pred[0], y_pred[0])

    def test_input_data_discrete(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender
        learner(data)

    def test_mrr(self, learner, filename, testdata=None):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender
        recommender = learner(data)

        # Check if there is a test dataset
        if testdata:
            data = Orange.data.Table(testdata)

        # Sample users
        num_users = len(recommender.U)
        num_samples = min(num_users, 1000)  # max. number to sample
        users_sampled = np.random.choice(np.arange(num_users), num_samples)

        # Compute MRR 1 - Check Orange.Table branch
        mrr1, _ = recommender.compute_mrr(data=data, users=users_sampled)
        print('MRR: %.4f' % mrr1)

        if not testdata:  # Extra checks
            # Compute MRR 2 - Check lil_matrix branch
            data, _, _ = preprocess(data)
            mrr2, _ = recommender.compute_mrr(data=data, users=users_sampled)

            # Compute MRR 3 - Check error branch
            self.assertRaises(TypeError,
                              lambda: recommender.compute_mrr(None, None))

        self.assertGreaterEqual(mrr1, 0)

    @unittest.skip("Skipping test")
    def test_CV(self, learner, filename):
        pass

    def test_warnings(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender and check warns
        self.assertWarns(UserWarning, learner, data)

        recommender = learner(data)
        arg = 'Something that is not a table'
        self.assertRaises(TypeError, recommender, arg)

    def test_divergence(self, learner, filename):
        # Load data
        data = Orange.data.Table(filename)

        # Train recommender and check divergence
        self.assertRaises(RuntimeError, lambda: learner(data))


if __name__ == "__main__":
    # Test all
    unittest.main()
