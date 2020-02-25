from pymongo import MongoClient


class Mongo(object):

    # create twitterdb database
    def database(self):
        client = MongoClient('localhost', 27017)
        return client.twitterdb

    # create tweets collection
    def collection(self):
        db = self.database()
        return db.tweets

