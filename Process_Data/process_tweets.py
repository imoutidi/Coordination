from Tool_Pack import tools
from pymongo import MongoClient, ASCENDING, errors
import tweepy
# import editdistance
# print(editdistance.eval('one banana', 'banana one'))
import os

class TextArchiver:
    def __init__(self):
        self.path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\" \
                          r"Climate_Changed\\"
        self.input_path = self.path + r"Downloaded_Tweets\\"
        self.output_path = self.path + r"I_O\\"

    def parse_tweets(self):
        for folder_index in range(16):
            for filename in os.listdir(self.input_path + str(folder_index)):
                tweets = tools.load_pickle(self.input_path + str(folder_index) + r"\\" + filename)

                print()

    def mongo_tester(self):
        client = MongoClient('localhost', 27017)
        db = client.Climate_Change_Tweets
        collection = db.tweet_documents
        collection.insert_one({"id": 200, "Author": "imoutidi", "Text": "Some tweet text here."})


if __name__ == "__main__":
    tweet_archiver = TextArchiver()
    # network_creator.parse_tweets()
    tweet_archiver.mongo_tester()
    print()