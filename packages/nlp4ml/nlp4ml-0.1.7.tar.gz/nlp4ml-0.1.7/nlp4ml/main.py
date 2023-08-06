import swifter
import pandas as pd
from preprocessing import clean_tweet, augment_text
from statistics import under_sampling


def main():
    dfx = pd.read_csv("./data/train.csv")
    dfx.tweet = dfx.tweet.swifter.apply(lambda x: clean_tweet(x, strip_punctuation=True))
    dfx["length"] = dfx["tweet"].swifter.apply(lambda x: len(x.split()))
    dfx = dfx[dfx.length >= 10].reset_index(drop=True)
    print(dfx.label.value_counts())
    dfx = augment_text(dfx, text_col="tweet", label_col="label", samples=12000)
    dfx = dfx[["tweet", "label"]]
    print(dfx)
    print(dfx.label.value_counts())


if __name__ == "__main__":
    main()
