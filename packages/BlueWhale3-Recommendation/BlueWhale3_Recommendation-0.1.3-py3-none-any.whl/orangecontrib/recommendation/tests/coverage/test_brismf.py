import Orange
from orangecontrib.recommendation.tests.coverage import TestRatingModels
from orangecontrib.recommendation import BRISMFLearner
from orangecontrib.recommendation.optimizers import *

import unittest

__dataset__ = 'ratings.tab'
__optimizers__ = [SGD(), Momentum(momentum=0.9),
                  NesterovMomentum(momentum=0.9), AdaGrad(),
                  RMSProp(rho=0.9), AdaDelta(rho=0.95),
                  Adam(beta1=0.9, beta2=0.999)]


class TestBRISMF(unittest.TestCase, TestRatingModels):

    def test_input_data_continuous(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1, min_rating=0,
                                max_rating=5, verbose=2,
                                callback=lambda x: None)

        # Test SGD optimizers too
        for opt in __optimizers__:
            learner.optimizer = opt
            print(learner.optimizer)
            super().test_input_data_continuous(learner, filename=__dataset__)

    def test_input_data_discrete(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1)
        super().test_input_data_discrete(learner, filename='ratings_dis.tab')

    def test_pairs(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1)
        super().test_pairs(learner, filename=__dataset__)

    def test_predict_items(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1)
        super().test_predict_items(learner, filename=__dataset__)

    def test_CV(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1)
        super().test_CV(learner, filename=__dataset__)

    def test_warnings(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1, learning_rate=0.0)
        super().test_warnings(learner, filename=__dataset__)

    def test_divergence(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1, learning_rate=1e20)
        super().test_divergence(learner, filename=__dataset__)

    def test_swap_columns(self, *args):
        learner = BRISMFLearner(num_factors=2, num_iter=1, random_state=42)
        super().test_swap_columns(learner, filename1='ratings_dis.tab',
                                  filename2='ratings_dis_swap.tab')

    def test_objective(self):
        from orangecontrib.recommendation.rating.brismf import compute_loss

        # Load data
        data = Orange.data.Table(__dataset__)

        steps = [1, 10, 30]
        objectives = []
        learner = BRISMFLearner(num_factors=2, learning_rate=0.0007,
                                random_state=42, verbose=False)

        for step in steps:
            learner.num_iter = step
            recommender = learner(data)

            # Set parameters
            bias = recommender.bias
            bias_t = (bias['globalAvg'], bias['dUsers'], bias['dItems'])
            low_rank_matrices = (recommender.P, recommender.Q)
            params = (learner.lmbda, learner.bias_lmbda)

            objective = compute_loss(data, bias_t, low_rank_matrices, params)
            objectives.append(objective)

        # Assert objective values decrease
        test = list(
            map(lambda t: t[0] >= t[1], zip(objectives, objectives[1:])))
        self.assertTrue(all(test))

        # ***** Test chunks - Just for coverage *****
        data = "Sth. error"
        self.assertRaises(TypeError, lambda: compute_loss(data, bias_t,
                                                          low_rank_matrices,
                                                          params))

    def test_outputs(self):
        # Load data
        data = Orange.data.Table(__dataset__)

        learner = BRISMFLearner(num_factors=2, num_iter=1)
        # Train recommender
        recommender = learner(data)

        # Check tables P and Q
        P = recommender.getPTable()
        Q = recommender.getQTable()

        diff = len({P.X.shape[1], Q.X.shape[1]})
        self.assertEqual(diff, 1)


if __name__ == "__main__":
    # # Test all
    # unittest.main()

    # Test single test
    suite = unittest.TestSuite()
    suite.addTest(TestBRISMF("test_divergence"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

