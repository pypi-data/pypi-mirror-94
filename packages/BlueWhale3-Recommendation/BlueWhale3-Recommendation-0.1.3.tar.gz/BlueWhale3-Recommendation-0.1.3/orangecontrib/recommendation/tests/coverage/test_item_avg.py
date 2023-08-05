from orangecontrib.recommendation.tests.coverage import TestRatingModels
from orangecontrib.recommendation import ItemAvgLearner

import unittest

__dataset__ = 'ratings.tab'


class TestItemAvg(unittest.TestCase, TestRatingModels):

    def test_input_data_continuous(self, *args):
        learner = ItemAvgLearner(verbose=True)
        super().test_input_data_continuous(learner, filename=__dataset__)

    def test_input_data_discrete(self, *args):
        learner = ItemAvgLearner()
        super().test_input_data_discrete(learner, filename='ratings_dis.tab')

    def test_pairs(self, *args):
        learner = ItemAvgLearner()
        super().test_pairs(learner, filename=__dataset__)

    def test_predict_items(self, *args):
        learner = ItemAvgLearner()
        super().test_predict_items(learner, filename=__dataset__)

    def test_swap_columns(self, *args):
        learner = ItemAvgLearner()
        super().test_swap_columns(learner, filename1='ratings_dis.tab',
                                  filename2='ratings_dis_swap.tab')

    def test_CV(self, *args):
        learner = ItemAvgLearner()
        super().test_CV(learner, filename=__dataset__)

    @unittest.skip("Skipping test")
    def test_warnings(self, *args):
        learner = ItemAvgLearner()
        super().test_warnings(learner, filename=__dataset__)

    @unittest.skip("Skipping test")
    def test_divergence(self, *args):
        learner = ItemAvgLearner()
        super().test_divergence(learner, filename=__dataset__)

if __name__ == "__main__":
    # Test all
    unittest.main()

    # # Test single test
    # suite = unittest.TestSuite()
    # suite.addTest(TestItemAvg("test_input_data_continuous"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

