import swifter
import pandas as pd
import numpy as np
from nlp4ml.preprocessing import clean_tweet, augment_text, KFold
from nlp4ml.ensembler import nested_cross_validation
from nlp4ml.statistics import under_sampling
from sklearn.tree import DecisionTreeClassifier


def main():
    dfx = pd.read_csv("./data/train.csv", nrows=1000)
    dfx.tweet = dfx.tweet.swifter.apply(lambda x: clean_tweet(x, strip_punctuation=True))
    dfx["length"] = dfx["tweet"].swifter.apply(lambda x: len(x.split()))
    dfx = dfx[dfx.length >= 10].reset_index(drop=True)
    samples = dfx.label.value_counts()[0] - dfx.label.value_counts()[1]
    dfx = augment_text(dfx, text_col="tweet", label_col="label", samples=samples)
    dfx = dfx[["tweet", "label"]]

    splitter = KFold(n_splits=5)
    dfx = splitter.split(dfx, target_col="label")
    
    model = DecisionTreeClassifier()
    space = {
        "max_depth": range(3, 5), 
        "min_sample_split": range(2, 4)
    }
    nested_cross_validation(model, 
                            space, 
                            dfx, 
                            target_col="label", 
                            inner_n_splits=5, 
                            outer_n_splits=3)


if __name__ == "__main__":
    main()
