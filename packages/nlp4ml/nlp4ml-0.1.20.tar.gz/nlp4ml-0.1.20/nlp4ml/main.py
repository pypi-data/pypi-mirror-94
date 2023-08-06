import swifter
import pandas as pd
import numpy as np
from pprint import pprint
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from gensim.models import KeyedVectors


from preprocessing import clean_tweet, augment_text, KFold
from ensembler import nested_cross_validation
from statistics import under_sampling
from vectoriser import SifEmbeddingVectorizer
from utils import seed_everything
seed_everything(seed=914)


def main():
    dfx = pd.read_csv("./data/train.csv", nrows=1000)
    dfx.tweet = dfx.tweet.swifter.apply(lambda x: clean_tweet(x, strip_punctuation=True))
    dfx["length"] = dfx["tweet"].swifter.apply(lambda x: len(x.split()))
    dfx = dfx[dfx.length >= 10].reset_index(drop=True)
    samples = dfx.label.value_counts()[0] - dfx.label.value_counts()[1]
    dfx = augment_text(dfx, text_col="tweet", label_col="label", samples=samples)
    dfx = dfx[["tweet", "label"]]

    WORD2VEC_PATH = r"./embedding/GoogleNews-vectors-negative300.bin"
    word2vec = KeyedVectors.load_word2vec_format(WORD2VEC_PATH, binary=True)
    sif_vectoriser = SifEmbeddingVectorizer(word2vec)

    tweet_tokenised = [tweet.split() for tweet in dfx.tweet.tolist()]
    tweet_vectorised = sif_vectoriser.fit_transform(tweet_tokenised, y=None)
    tweet_vectorised_df = pd.DataFrame(tweet_vectorised)
    dfx = pd.concat([tweet_vectorised_df, dfx.label], axis=1)
    
    model = DecisionTreeClassifier()
    space = {
        "max_depth": range(3, 5), 
        "min_samples_split": range(2, 4)
    }

    results = nested_cross_validation(model, 
                                      space, 
                                      X=tweet_vectorised, 
                                      y=dfx.label, 
                                      target_col="label", 
                                      inner_n_splits=5, 
                                      outer_n_splits=3)
    pprint(results)


if __name__ == "__main__":
    main()
