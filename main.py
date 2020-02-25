from tweepy import OAuthHandler
from mylistener import MyListener
from mongo import Mongo
from tweepy import Stream
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def setup_api_twitter():

    # INFO: This section should be replaced by the information about your own twitter app.
    # The access_token and access_token_secret here informed is not available anymore.

    consumer_key = 'lcHXCo5f6s1DFpegvViDIEYnc'
    consumer_secret_key = 'acDTn4yAG290vd9j38ugE43rLSmIVKsJYzRDr3ODzlFVcoGElI'
    access_token = '35552990-SpOfykeTUmAl0A5B9bqGeY5yZMSBketmK70tVGjw1'
    access_token_secret = 'ukMWOcimzNQ8c1QL5P2HxEbmDEKudhnse9W125vuxLJwZ'

    auth = OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    return auth


if __name__ == '__main__':

    m = Mongo()
    col = m.collection()

    my_listener = MyListener(0, 20, col)
    auth = setup_api_twitter()
    keywords = ['bbb', 'bbb20', 'pyong', 'prior']

    # Convert a collection of text documents to a matrix of token counts
    cv = CountVectorizer()

    # http://docs.tweepy.org/en/latest/streaming_how_to.html
    my_stream = Stream(auth, listener=my_listener)
    my_stream.filter(track=keywords)
    my_stream.disconnect()

    # list comprehension
    # structure: [output expression + loop (for .. in) + conditional (if exists)]
    data_set = [{'create_at': item['created_at'], 'text': item['text']} for item in col.find()]

    # transforming data_set into pandas data frame
    df = pd.DataFrame(data_set)

    # fit_transform = Learn the vocabulary dictionary and return term-document matrix.
    count_matrix = cv.fit_transform(df.text)
    # print(count_matrix.toarray())

    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
    # get_feature_names = Array mapping from feature integer indices to feature name.
    # print(cv.get_feature_names())

    # set data frame with column "words" containing all words from my df
    word_count = pd.DataFrame(cv.get_feature_names(), columns=["words"])
    # count how many times a word appears
    word_count["count"] = count_matrix.sum(axis=0).tolist()[0]
    # sorting
    word_count = word_count.sort_values("count", ascending=False).reset_index(drop=True)
    # show 50 words
    print(word_count[:50])

