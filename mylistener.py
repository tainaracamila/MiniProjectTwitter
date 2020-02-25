import json
from tweepy import StreamListener


class MyListener (StreamListener):

    # min_tweets = minimum number of tweets to stream
    # max_tweets = maximum number of tweets to stream
    # col = mongodb collection
    def __init__(self, min_tweets, max_tweets, col):
        super().__init__()
        self.min_tweets = min_tweets
        self.max_tweets = max_tweets
        self.col = col

    def on_data(self, data):
        tweet = json.loads(data)
        created_at = tweet['created_at']
        id_str = tweet['id_str']
        text = tweet['text']

        obj = {'created_at': created_at,
               'id_str': id_str,
               'text': text}

        if self.min_tweets <= self.max_tweets:
            self.col.insert_one(obj)
            self.min_tweets += 1
            return True
        else:
            return False


