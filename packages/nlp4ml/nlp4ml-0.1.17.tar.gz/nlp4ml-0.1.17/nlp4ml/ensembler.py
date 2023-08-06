import numpy as np
import pandas as pd
from sklearn.tree import ExtraTreeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import OneClassSVM
from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from sklearn.neighbors.classification import RadiusNeighborsClassifier
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.multioutput import ClassifierChain
from sklearn.multioutput import MultiOutputClassifier
from sklearn.multiclass import OutputCodeClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model.stochastic_gradient import SGDClassifier
from sklearn.linear_model.ridge import RidgeClassifierCV
from sklearn.linear_model.ridge import RidgeClassifier
from sklearn.linear_model.passive_aggressive import PassiveAggressiveClassifier
from sklearn.gaussian_process.gpc import GaussianProcessClassifier
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.ensemble.bagging import BaggingClassifier
from sklearn.ensemble.forest import ExtraTreesClassifier
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import GaussianNB
from sklearn.semi_supervised import LabelPropagation
from sklearn.semi_supervised import LabelSpreading
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import NearestCentroid
from sklearn.svm import NuSVC
from sklearn.linear_model import Perceptron
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from nlp4ml.preprocessing import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import metrics
from collections import defaultdict

def nested_cross_validation(model, 
							space, 
							df, 
							target_col, 
							inner_n_splits, 
							outer_n_splits, 
							grid=True, 
							scoring="accuracy"):
	results = defaultdict(list)
	splitter = KFold(inner_n_splits, task="classification")
	df = splitter.split(df, target_col, shuffle=True)
	for fold in range(inner_n_splits):
		results["fold"].append(fold)
		df_train = df[df["kfold"]!=fold]
		df_valid = df[df["kfold"]==fold]
		X_train = df_train.loc[:, df_train.columns!=target_col]
		X_valid = df_valid.loc[:, df_valid.columns!=target_col]
		y_train = df_train.loc[:, df_train.columns==target_col]
		y_valid = df_valid.loc[:, df_valid.columns==target_col]

		assert isinstance(space, dict), "Space must be a dictionary!"
		if grid == True:
			search = GridSearchCV(model, 
								  space, 
								  scoring=scoring, 
								  cv=inner_n_splits, 
								  refit=True)
		elif grid == False:
			search = RandomizedSearchCV(model, 
										space, 
										scoring=scoring, 
										cv=inner_n_splits, 
										refit=True)
		result = search.fit(X_train, y_train)
		best_model = result.best_estimator_
		y_hat = best_model.predict(X_valid)

		acc = metrics.accuracy_score(y_valid, y_hat)
		f1 = metrics.f1_score(y_valid, y_hat)
		precision = metrics.precision_score(y_valid, y_hat)
		recall = metrics.recall_score(y_valid, y_hat)
		results["acc"].append(acc)
		results["f1"].append(f1)
		results["precision"].append(precision)
		results["recall"].append(recall)

		print("="*50)
		print(f"Fold {fold}")
		print("Accuracy={:.4f}\nF1={:.4f}\nPrecision={:.4f}\nRecall={:.4f}".format(
			acc, f1, precision, recall))
		print("Best Score={:.4f}\nParams={}".format(
			result.best_score_, result.best_params_))
		print("="*50)

	print('\nAccuracy: %.4f (±%.4f)' % (np.mean(results["acc"]), np.std(results["acc"])))
	return