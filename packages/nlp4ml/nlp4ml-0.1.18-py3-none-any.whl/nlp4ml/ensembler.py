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
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn import metrics
from collections import defaultdict


from preprocessing import KFold


def nested_cross_validation(model, 
                            space, 
                            df=None, 
                            target_col=None, 
                            X=None, y=None, 
                            inner_n_splits=3, 
                            outer_n_splits=5, 
                            mode="grid", 
                            scoring="accuracy"):
    """
    Parameters
    ----------
    model: estimator object
        This is assumed to implement the scikit-learn estimator interface.
    space: dict
        Parameters distribution dictionary.
    df: pd.DataFrame
        A pd.DataFrame contains features and label.
    target_col: str
        Label name.
    inner_n_splits: int
        The value for the inner loop (for parameter search).
    outer_n_splits: int
        The value for the outer loop (for k-fold cross validation).
    mode: str {"grid", "random"}
        Utilise GridSearchCV() or RandomizedSearchCV()
    scoring: str {"accuracy", "balanced_accuracy", "f1", "roc_auc", ...}
        https://scikit-learn.org/stable/modules/model_evaluation.html

    Returns
    -------
    results: defaultdict

    Examples
    --------
    >>> model = DecisionTreeClassifier()
    >>> space = {
            "max_depth": range(3, 5), 
            "min_samples_split": range(2, 4)
        }
    >>> results = nested_cross_validation(model, 
                                          space, 
                                          dfx, 
                                          target_col="label", 
                                          inner_n_splits=5, 
                                          outer_n_splits=3)
    """
    results = defaultdict(list)
    splitter = KFold(inner_n_splits, task="classification")
    if (X is None) and (y is None):
        df = splitter.split_df(df, target_col, shuffle=True)
    else:
        df = splitter.split_X_y(X, y, shuffle=True)

    for fold in range(inner_n_splits):
        df_train = df[df["kfold"]!=fold]
        df_valid = df[df["kfold"]==fold]
        X_train = df_train.loc[:, df_train.columns!=target_col]
        X_valid = df_valid.loc[:, df_valid.columns!=target_col]
        y_train = df_train.loc[:, df_train.columns==target_col]
        y_valid = df_valid.loc[:, df_valid.columns==target_col]

        assert isinstance(space, dict), "Space must be a dictionary!"
        if mode == "grid":
            search = GridSearchCV(model, 
                                  space, 
                                  scoring=scoring, 
                                  cv=inner_n_splits, 
                                  refit=True)
        elif mode == "random":
            search = RandomizedSearchCV(model, 
                                        space, 
                                        scoring=scoring, 
                                        cv=inner_n_splits, 
                                        refit=True)
        elif mode == "bayes":
            "Bayes mode has not been implemented yet..."

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
        print(f"Fold {fold+1}")
        print("Accuracy={:.4f}\nF1={:.4f}\nPrecision={:.4f}\nRecall={:.4f}".format(
            acc, f1, precision, recall))
        print("Best Score={:.4f}\nParams={}".format(
            result.best_score_, result.best_params_))
        print("="*50)

    print('\nAccuracy: %.4f (±%.4f)' % (np.mean(results["acc"]), np.std(results["acc"])))
    return results