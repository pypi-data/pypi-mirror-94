import Orange
from Orange.evaluation.testing import CrossValidation
from orangecontrib.recommendation import *

from sklearn.metrics import mean_squared_error, mean_absolute_error

import math
import time


def test_learners():
    start = time.time()

    # Load data
    #data = Orange.data.Table('epinions_test.tab')
    data = Orange.data.Table('filmtrust/ratings.tab')
    trust = Orange.data.Table('filmtrust/trust.tab')

    print('- Loading time: %.3fs' % (time.time() - start))


    # Global average
    start = time.time()
    learner = GlobalAvgLearner()
    recommender = learner(data)
    print('- Time (GlobalAvgLearner): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (GlobalAvgLearner): %.3f' % rmse)
    print('- MAE (GlobalAvgLearner): %.3f' % mae)
    print('')

    # Item average
    start = time.time()
    learner = ItemAvgLearner()
    recommender = learner(data)
    print('- Time (ItemAvgLearner): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (ItemAvgLearner): %.3f' % rmse)
    print('- MAE (ItemAvgLearner): %.3f' % mae)
    print('')

    # User average
    start = time.time()
    learner = UserAvgLearner()
    recommender = learner(data)
    print('- Time (UserAvgLearner): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (UserAvgLearner): %.3f' % rmse)
    print('- MAE (UserAvgLearner): %.3f' % mae)
    print('')

    # User-Item baseline
    start = time.time()
    learner = UserItemBaselineLearner()
    recommender = learner(data)
    print('- Time (UserItemBaselineLearner): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (UserItemBaselineLearner): %.3f' % rmse)
    print('- MAE (UserItemBaselineLearner): %.3f' % mae)
    print('')

    # BRISMF
    start = time.time()
    learner = BRISMFLearner(num_factors=10, num_iter=15, learning_rate=0.01,
                            lmbda=0.1, verbose=0)
    recommender = learner(data)
    print('- Time (BRISMFLearner): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (BRISMFLearner): %.3f' % rmse)
    print('- MAE (BRISMFLearner): %.3f' % mae)
    print('')

    # SVD++
    start = time.time()
    learner = SVDPlusPlusLearner(num_factors=10, num_iter=15,
                                 learning_rate=0.01, lmbda=0.1, verbose=0)
    recommender = learner(data)
    print('- Time (SVDPlusPlusLearner): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (SVDPlusPlusLearner): %.3f' % rmse)
    print('- MAE (SVDPlusPlusLearner): %.3f' % mae)
    print('')

    # TrustSVD
    start = time.time()
    learner = TrustSVDLearner(num_factors=10, num_iter=15, learning_rate=0.01,
                              lmbda=0.12, social_lmbda=0.9, trust=trust,
                              verbose=0)
    recommender = learner(data)
    print('- Time (TrustSVD): %.3fs' % (time.time() - start))
    rmse = math.sqrt(mean_squared_error(data.Y, recommender(data)))
    mae = mean_absolute_error(data.Y, recommender(data))
    print('- RMSE (TrustSVD): %.3f' % rmse)
    print('- MAE (TrustSVD): %.3f' % mae)
    print('')


def test_CV():

    # Load data
    data = Orange.data.Table('filmtrust/ratings_small.tab')
    trust = Orange.data.Table('filmtrust/trust_small.tab')

    # Learners
    global_avg = GlobalAvgLearner()
    items_avg = ItemAvgLearner()
    users_avg = UserAvgLearner()
    useritem_baseline = UserItemBaselineLearner()
    brismf = BRISMFLearner(num_factors=15, num_iter=10, learning_rate=0.07,
                           lmbda=0.1)
    svdpp = SVDPlusPlusLearner(num_factors=15, num_iter=10, learning_rate=0.007,
                               lmbda=0.1)
    trustsvd = TrustSVDLearner(num_factors=15, num_iter=10, learning_rate=0.007,
                               lmbda=0.1, social_lmbda=0.05, trust=trust)
    learners = [global_avg, items_avg, users_avg, useritem_baseline,
                brismf, svdpp, trustsvd]

    res = CrossValidation(data, learners, k=5)
    rmse = Orange.evaluation.RMSE(res)
    r2 = Orange.evaluation.R2(res)

    print("Learner  RMSE  R2")
    for i in range(len(learners)):
        print(
            "{:8s} {:.2f} {:5.2f}".format(learners[i].name, rmse[i], r2[i]))

if __name__ == "__main__":
    #pass
    test_learners()