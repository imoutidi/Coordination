from Tool_Pack import tools
from pymongo import MongoClient, ASCENDING, errors
import tweepy
# import editdistance
# print(editdistance.eval('one banana', 'banana one'))
import os

import nltk
# nltk.download('stopwords')  # download stopwords corpus
# nltk.download('punkt')  # download punkt tokenizer
# nltk.download('wordnet')  # download WordNet lemmatizer

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TweetArchiver:
    def __init__(self):
        self.path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\" \
                          r"Climate_Changed\\"
        self.input_path = self.path + r"Downloaded_Tweets\\"
        self.output_path = self.path + r"I_O\\"
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.Climate_Change_Tweets
        self.collection = self.db.tweet_documents

    @staticmethod
    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.lower() not in stop_words]
        filtered_text = ' '.join(filtered_words)
        return filtered_text

    @staticmethod
    def stop_words_and_lemmatize(text):
        # Tokenize the text
        words = word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

        # Join the words back into a string
        preprocessed_text = ' '.join(lemmatized_words)
        return preprocessed_text

    def parse_tweets(self):
        set_of_tweets = set()
        for folder_index in range(16):
            print(folder_index)
            for filename in os.listdir(self.input_path + str(folder_index)):
                tweet_records = tools.load_pickle(self.input_path + str(folder_index) + r"\\" + filename)
                for tweet_obj in tweet_records:
                    if tweet_obj.id in set_of_tweets:
                        continue
                    else:
                        set_of_tweets.add(tweet_obj.id)
                        self.mongo_insert(tweet_obj)

    def mongo_insert(self, tweet_object):
        author_username = tweet_object.author.name
        author_id = tweet_object.author.id
        full_text = tweet_object.full_text
        tweet_id = tweet_object.id
        tweet_date = tweet_object.created_at
        # tweet_id will be an index in the database.
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