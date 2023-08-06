import swifter
import pandas as pd
from preprocessing import clean_tweet


def main():
    dfx = pd.read_csv("./data/train.csv")
    dfx.tweet = dfx.tweet.swifter.apply(lambda x: clean_tweet(x, strip_punctuation=True))
    dfx = dfx.sample(100)
    for doc in dfx.tweet:
        print(doc)
        print("-"*50)


if __name__ == "__main__":
    main()
