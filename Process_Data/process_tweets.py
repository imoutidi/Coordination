from Tool_Pack import tools
from pymongo import MongoClient, ASCENDING, errors
import tweepy
# import editdistance
# print(editdistance.eval('one banana', 'banana one'))
import os


class TweetArchiver:
    def __init__(self):
        self.path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\" \
                          r"Climate_Changed\\"
        self.input_path = self.path + r"Downloaded_Tweets\\"
        self.output_path = self.path + r"I_O\\"
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.Climate_Change_Tweets
        self.collection = self.db.tweet_documents

    def parse_tweets(self):
        for folder_index in range(16):
            print(folder_index)
            for filename in os.listdir(self.input_path + str(folder_index)):
                tweet_records = tools.load_pickle(self.input_path + str(folder_index) + r"\\" + filename)
                for tweet_obj in tweet_records:
                    self.mongo_insert(tweet_obj)

    def mongo_insert(self, tweet_object):
        author_username = tweet_object.author.name
        author_id = tweet_object.author.id
        full_text = tweet_object.full_text
        tweet_id = tweet_object.id
        tweet_date = tweet_object.created_at
        try:
            self.collection.insert_one({"author_id": author_id, "author_username": author_username,
                                        "full_text": full_text, "tweet_id": tweet_id, "tweet_date": tweet_date})
        except errors.DuplicateKeyError as key_error:
            print(key_error)
            print(tweet_id)


if __name__ == "__main__":
    climate_change_archiver = TweetArchiver()
    climate_change_archiver.parse_tweets()
    print()