import os
import pandas as pd
import requests
import json
import csv
import time
import datetime
import praw
from dateutil.relativedelta import relativedelta
from Tool_Pack import tools
from prawcore.exceptions import Forbidden




def getPushshiftData():
    url = " https://api.pushshift.io/reddit/search/submission/?limit=1000&q=trump&after=1514764800&before=1517443200&subreddit=politics"
    url1 = "https://api.pushshift.io/reddit/search/submission/?ids=125udaj"
    print(url)
    r = requests.get(url1)
    posts = json.loads(r.text)
    for r_post in posts["data"]:
        if "body" in r_post:
            print()
    return posts["data"]


def get_post_with_id(post_id="125udaj"):
    url = f"https://api.pushshift.io/reddit/submission/search/?ids={post_id}"
    response = requests.get(url)
    post = None
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"]:
            post = data["data"][0]  # The first item in the "data" array contains the post data
        else:
            print("Post not found")
    else:
        print(f"Error: {response.status_code}")
    return post


# Getting submission ids for 6 hour time interval for a given date range
def get_submissions_records_for_time_range(start_date_str, end_date_str, subreddit_name, query=None):
    hour_interval = 3
    start_date_obj = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date_obj = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    earlier_date = start_date_obj
    later_date = start_date_obj + relativedelta(hours=hour_interval)
    batch_size = 1000  # Number of submissions to retrieve per request

    url_template = "https://api.pushshift.io/reddit/search/submission/?size={}&after={}&before={}&subreddit={}"
    if query is not None:
        url_template += "&q=" + query

    submission_records = list()

    # Send requests to API in batches until all submissions have been retrieved
    while earlier_date <= end_date_obj:
        # pushshift allows 1 request per second but let don't strain their system.
        time.sleep(1.1)
        # Construct the URL for the API endpoint with the current pagination parameters
        url = url_template.format(batch_size, date_converter(earlier_date), date_converter(later_date), subreddit_name)

        # Send a GET request to the API endpoint
        response = requests.get(url)
        print()

        # Extract the ids of the submissions from the response JSON
        # submission_ids += [submission["id"] for submission in response.json()["data"]]
        sub_list = list()
        try:
            sub_list = response.json()["data"]
        except requests.exceptions.JSONDecodeError as json_error:
            print(json_error)
            print(response)

        for submission in sub_list:
            fields_dict = dict()
            if "author" in submission:
                fields_dict["author"] = submission["author"]
            else:
                fields_dict["author"] = "N_A"
            if "author_fullname" in submission:
                fields_dict["author_fullname"] = submission["author_fullname"]
            else:
                fields_dict["author_fullname"] = "N_A"
            if "id" in submission:
                fields_dict["id"] = submission["id"]
            else:
                fields_dict["id"] = "N_A"
            if "permalink" in submission:
                fields_dict["permalink"] = submission["permalink"]
            else:
                fields_dict["permalink"] = "N_A"
            if "retrieved_uts" in submission:
                fields_dict["retrieved_utc"] = submission["retrieved_utc"]
            else:
                fields_dict["retrieved_utc"] = "N_A"
            if "score" in submission:
                fields_dict["score"] = submission["score"]
            else:
                fields_dict["score"] = "N_A"
            if "selftext" in submission:
                fields_dict["selftext"] = submission["selftext"]
            else:
                fields_dict["selftext"] = "N_A"
            if "subreddit" in submission:
                fields_dict["subreddit"] = submission["subreddit"]
            else:
                fields_dict["subreddit"] = "N_A"
            if "title" in submission:
                fields_dict["title"] = submission["title"]
            else:
                fields_dict["title"] = "N_A"
            if "url" in submission:
                fields_dict["url"] = submission["url"]
            else:
                fields_dict["url"] = "N_A"
            if "utc_datetime_str" in submission:
                fields_dict["utc_datetime_str"] = submission["utc_datetime_str"]
            else:
                fields_dict["utc_datetime_str"] = "N_A"
            submission_records.append(fields_dict)

        if len(sub_list) == batch_size:
            print("Batch size limit reached.")

        # print(str(len(submission_ids)))
        # print("Updated date: " + str(start_epoch))

        print(earlier_date)
        earlier_date = later_date
        later_date += relativedelta(hours=hour_interval)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\New_Submissions\\"
                      + subreddit_name + "_" + start_date_str + "_" + end_date_str, submission_records)


def date_converter(date_obj):
    timestamp = int(time.mktime(date_obj.timetuple()))
    return timestamp


def get_submissions_with_praw():
    subreddit_name = "cryptocurrency"
    time_period = "year"
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.top(time_filter=time_period, limit=None)
    submission_records = list()
    counter = 0
    for submission in submissions:
        # time.sleep(0.1)
        fields_dict = dict()
        if hasattr(submission, "author"):
            fields_dict["author"] = submission.author
        else:
            fields_dict["author"] = "N_A"
        if hasattr(submission, "author_fullname"):
            fields_dict["author_fullname"] = submission.author_fullname
        else:
            fields_dict["author_fullname"] = "N_A"
        if hasattr(submission, "id"):
            fields_dict["id"] = submission.id
        else:
            fields_dict["id"] = "N_A"
        if hasattr(submission, "permalink"):
            fields_dict["permalink"] = submission.permalink
        else:
            fields_dict["permalink"] = "N_A"
        if hasattr(submission, "retrieved_utc"):
            fields_dict["retrieved_utc"] = submission.retrieved_utc
        else:
            fields_dict["retrieved_utc"] = "N_A"
        if hasattr(submission, "score"):
            fields_dict["score"] = submission.score
        else:
            fields_dict["score"] = "N_A"
        if hasattr(submission, "selftext"):
            fields_dict["selftext"] = submission.selftext
        else:
            fields_dict["selftext"] = "N_A"
        if hasattr(submission, "subreddit"):
            fields_dict["subreddit"] = submission.subreddit
        else:
            fields_dict["subreddit"] = "N_A"
        if hasattr(submission, "title"):
            fields_dict["title"] = submission.title
        else:
            fields_dict["title"] = "N_A"
        if hasattr(submission, "url"):
            fields_dict["url"] = submission.url
        else:
            fields_dict["url"] = "N_A"
        if hasattr(submission, "utc_datetime_str"):
            fields_dict["utc_datetime_str"] = submission.utc_datetime_str
        else:
            fields_dict["utc_datetime_str"] = "N_A"
        submission_records.append(fields_dict)
        if counter % 10 == 0 and counter != 0:
            tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                              r"New_Submissions\\" + str(counter) + "_submissions", submission_records)
            submission_records = list()
        print(counter)
        counter += 1


def retrieve_comments_ids_per_submission():
    period_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                                       r"New_Submissions\worldnews_2022-01-01_2022-05-01")
    # period_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Twitter_Parser\I_O\\"
    #                                    r"Politics\January_6_United_States_Capitol_attack\submission_records")
    # period_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Covid\\"
    #                                    r"r_science_submission_records")

    # TODO change that to zero when starting the scraper
    idx_correction = 0
    submission_id_to_comments_dict = dict()
    for idx, sub_record in enumerate(period_records[idx_correction:]):
        if (idx + idx_correction) % 1000 == 0:
            print("Saved until idx:" + str(idx + idx_correction))
            tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                              r"Comments\New_Comments\comments_2022-05-01_"
                              + str(idx + idx_correction), submission_id_to_comments_dict)
            submission_id_to_comments_dict = dict()
        comment_list = list()
        try:
            submission = reddit.submission(sub_record["id"])
            # print()
        except Forbidden as f_error:
            print(f_error)
        # submission.comments.replace_more(limit=None, threshold=0)
        for comment in submission.comments.list():
            # for reply in comment.replies.list():
            #     print()
            comment_record_dict = dict()
            if "id" in comment.__dict__:
                comment_record_dict["id"] = comment.__dict__["id"]
            else:
                comment_record_dict["id"] = "N_A"
            if "subreddit" in comment.__dict__:
                comment_record_dict["subreddit"] = comment.__dict__["subreddit"]
            else:
                comment_record_dict["subreddit"] = "N_A"
            if "author" in comment.__dict__:
                comment_record_dict["author"] = comment.__dict__["author"]
            else:
                comment_record_dict["author"] = "N_A"
            if "score" in comment.__dict__:
                comment_record_dict["score"] = comment.__dict__["score"]
            else:
                comment_record_dict["score"] = "N_A"
            if "author_fullname" in comment.__dict__:
                comment_record_dict["author_fullname"] = comment.__dict__["author_fullname"]
            else:
                comment_record_dict["author_fullname"] = "N_A"
            if "body" in comment.__dict__:
                comment_record_dict["body"] = comment.__dict__["body"]
            else:
                comment_record_dict["body"] = "N_A"
            if "permalink" in comment.__dict__:
                comment_record_dict["permalink"] = comment.__dict__["permalink"]
            else:
                comment_record_dict["permalink"] = "N_A"
            if "created_utc" in comment.__dict__:
                comment_record_dict["created_utc"] = comment.__dict__["created_utc"]
            else:
                comment_record_dict["created_utc"] = "N_A"
            if "parent_id" in comment.__dict__:
                comment_record_dict["parent_id"] = comment.__dict__["parent_id"]
            else:
                comment_record_dict["parent_id"] = "N_A"
            comment_list.append(comment_record_dict)
        submission_id_to_comments_dict[sub_record["id"]] = comment_list
        time.sleep(4)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                              r"Comments\New_Comments\comments_2022-05-01_last", submission_id_to_comments_dict)

    # ///////////////////////////////////////////////////////////
    # pushshift comment_ids is broken at the moment
    # url_template = "https://api.pushshift.io/reddit/submission/comment_ids/{}"
    # for r_post in period_record:
    #     url = url_template.format(r_post["id"])
    #     # Send a GET request to the API endpoint
    #     print(int('103k1qe', 36))
    #     url = "https://api.pushshift.io/reddit/submission/comment_ids/" + str(int('103k1qe', 36)) + "&q=*"
    #     response = requests.get(url)
    #     print()


def merge_crypto_submissions():
    input_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\New_Submissions\\"
    merged_submissions = list()
    for filename in os.listdir(input_path):
        submissions = tools.load_pickle(input_path + filename)
        for sub in submissions:
            merged_submissions.append(sub)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                      r"New_Submissions\\All_submissions2", merged_submissions)


def compare_submission_ids():
    sub_set_1 = set()
    sub_set_2 = set()
    result_set = sub_set_1.intersection(sub_set_2)


if __name__ == "__main__":
    # getPushshiftData()
    # get_post_with_id()
    # get_submissions_records_for_time_range("2022-06-07", "2023-06-07", "CryptoCurrency")
    get_submissions_with_praw()
    # retrieve_comments_ids_per_submission()
    # merge_crypto_submissions()
    # a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\New_Submissions\All_submissions")
    # b = get_post_with_id("119wltg")
    print()

