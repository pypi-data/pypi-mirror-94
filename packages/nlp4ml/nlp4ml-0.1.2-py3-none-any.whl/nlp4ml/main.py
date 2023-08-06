import pandas as pd
import numpy as np
from search import hyperparameters
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    dfx = pd.read_csv("./data/train.csv")
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(dfx.tweet)
    y_train = dfx.label.values
    xgb = XGBClassifier(verbosity=0)
    space = {
        'eta': np.arange(0.1, 0.26, 0.05),
        'min_child_weight': np.arange(1, 5, 0.5),
        'gamma': [5],
        'subsample': np.arange(0.5, 1.0, 0.11),
        'colsample_bytree': np.arange(0.5, 1.0, 0.11),
        'max_depth': range(2, 10, 1),
        'n_estimators': range(60, 220, 40),
        'learning_rate': [0.1, 0.01, 0.05]
    }

    hyperparameters(xgb,
                    space,
                    X_train,
                    y_train,
                    n_iter=10,
                    kfold=3,
                    scoring='f1')


if __name__ == "__main__":
    main()
