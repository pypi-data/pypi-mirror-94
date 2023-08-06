import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def get_best_hyperparams(model, hyperparameters_space, trainX, trainY, kfold=10):
    gs = GridSearchCV(model, 
                          param_grid = hyperparameters_space, 
                          scoring    = "neg_mean_squared_error",
                          n_jobs     = -1, 
                          cv         = kfold, 
                          refit      = False, 
                          return_train_score=True)
    gs.fit(trainX, trainY)
    return gs.best_params_

def MLR(X, y, test_size=0.6):
    trainX, testX, trainY, testY = train_test_split(X, y, test_size = test_size)
    # linear regression model for TRAIN
    lm = LinearRegression(normalize = True)
    lm.fit(trainX, trainY)
    y_pred_mlr = lm.predict(testX)
    # errors and r2 for TEST
    RMSE = np.sqrt(metrics.mean_squared_error(testY, y_pred_mlr))
    R2   = metrics.r2_score(testY, y_pred_mlr)
    # parameters
    coef     = lm.coef_
    inte     = lm.intercept_
    # prediction
    y_pred = lm.predict(X)
    return dict(name = 'MLR', y_pred = y_pred.ravel(), RMSE = RMSE, R2 = R2, model=lm, hparams=dict(coef = coef, intercept=inte))

def KNN(X, y, test_size=0.6, kfold=10):
    trainX, testX, trainY, testY = train_test_split(X, y, test_size = test_size)
    # range of hyperparams
    neighs        = np.arange(1, 8)
    pow_distance  = np.arange(1, 3)
    hyperp_space  = {'n_neighbors' : neighs, 'p': pow_distance}
    knn_estimator = KNeighborsRegressor()
    # get best hyperparams
    best_hyper_params = get_best_hyperparams(knn_estimator, hyperp_space, trainX, trainY)
    # fit for TRAIN
    knn_estimator = KNeighborsRegressor(**best_hyper_params)
    knn_estimator.fit(trainX, trainY)
    # prediction
    y_pred = knn_estimator.predict(testX)
    # RMSE, MAE and R2 for TEST
    RMSE = np.sqrt(metrics.mean_squared_error(testY, y_pred))
    MAE  = metrics.mean_absolute_error(testY, y_pred)
    R2   = metrics.r2_score(testY, y_pred)
    # prediction
    y_pred = knn_estimator.predict(X)

    return dict(name='KNN', y_pred=y_pred.ravel(), RMSE=RMSE, R2=R2, MAE=MAE, model=knn_estimator, hparams=best_hyper_params)

def RFO(X, y, test_size=0.6, kfold=10):
    trainX, testX, trainY, testY = train_test_split(X, y, test_size = test_size)
    # hyperparameters space
    n_estimators = [16 , 32, 50, 100, 250]
    max_features = [1,2,3]
    max_depth    = [3,5,7,10]
    hyperp_space = {'n_estimators' : n_estimators, 'max_features': max_features, 'max_depth': max_depth}
    rfo_estimator = RandomForestRegressor()
    # k-fold cross-validation
    #gs_rfo = GridSearchCV(rfo_estimator, scoring = 'neg_mean_squared_error', n_jobs=-1, param_grid = hyperp_space, cv = kfold, refit = False)
    #gs_rfo.fit(trainX, trainY.values.ravel())
    best_hyperparams = get_best_hyperparams(rfo_estimator, hyperp_space, trainX, trainY.values.ravel())
    rfo_estimator = RandomForestRegressor(**best_hyperparams)
    # fit with TRAIN
    rfo_estimator.fit(trainX, trainY.values.ravel())
    # testing
    y_pred = rfo_estimator.predict(testX)

    # errors
    RMSE = np.sqrt(metrics.mean_squared_error(testY, y_pred))
    MAE  = metrics.mean_absolute_error(testY, y_pred)
    R2   = metrics.r2_score(testY, y_pred)

    # complete y_pred
    y_pred = rfo_estimator.predict(X)
    
    return dict(name='RFO', y_pred=y_pred.ravel(), RMSE=RMSE, R2=R2, MAE=MAE, model=rfo_estimator, hparams=best_hyperparams)

def SVR(X, y, test_size=0.6, kfold=10):
    trainX, testX, trainY, testY = train_test_split(X, y, test_size = test_size)
    # hyperparameters space
    cs           = [0.1, 1.0, 10.0, 1000.0]
    gs           = np.arange(start=0.1, stop = 2.0, step=0.2)
    epsilons     = np.arange( start = 0.01, stop = 0.1, step = 0.01)
    hyperp_space  = {'C': cs, 'gamma': gs, 'epsilon': epsilons} 
    svr_estimator = svm.SVR()
    # k-fold cross-validation
    #gs_svr = GridSearchCV(svr_estimator, scoring = 'neg_mean_squared_error', n_jobs=-1, param_grid = hyperp_space, cv = kfold, refit = True )
    #gs_svr.fit(trainX, trainY.values.ravel())
    best_hyperparams = get_best_hyperparams(svr_estimator, hyperp_space, trainX, trainY.values.ravel())
    svr_estimator = svm.SVR(**best_hyperparams) #C = best_c, gamma = best_gamma, epsilon = best_eps)
    # trainning
    svr_estimator.fit(trainX, trainY.values.ravel())
    # testing
    y_pred = svr_estimator.predict(testX)
    # errors
    RMSE = np.sqrt(metrics.mean_squared_error(testY, y_pred))
    MAE  = metrics.mean_absolute_error(testY, y_pred)
    R2   = metrics.r2_score(testY, y_pred)
    # prediction
    y_pred = svr_estimator.predict(X)

    return dict(name='SVR', y_pred=y_pred, RMSE=RMSE, R2=R2, MAE=MAE, model=svr_estimator, hparams=best_hyperparams)

