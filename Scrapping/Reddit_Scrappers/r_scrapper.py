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


reddit = praw.Reddit(client_id="JA5vOF4gOhcjuGqdHU2Gcw", client_secret="3XT735o7Yc5dPql4EG9ThcqVgzrPZw",
                     user_agent="Climate_Change")

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


def get_post_with_id():
    post_id = "125udaj"  # Replace with the ID of the post you are looking for

    url = f"https://api.pushshift.io/reddit/submission/search/?ids={post_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"]:
            post = data["data"][0]  # The first item in the "data" array contains the post data
            print(post)
        else:
            print("Post not found")
    else:
        print(f"Error: {response.status_code}")


# Getting submission ids for 6 hour time interval for a give date range
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
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Covid\r_"
                      + subreddit_name + "_submission_records", submission_records)


def date_converter(date_obj):
    timestamp = int(time.mktime(date_obj.timetuple()))
    return timestamp


def retrieve_comments_ids_per_submission():
    # period_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Twitter_Parser\I_O\\"
    #                                    r"Politics\January_6_United_States_Capitol_attack\submission_records")
    period_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Covid\\"
                                       r"r_science_submission_records")

    # TODO change that to zero when starting the scraper
    idx_correction = 0
    submission_id_to_comments_dict = dict()
    for idx, sub_record in enumerate(period_records[idx_correction:]):
        if (idx + idx_correction) % 10 == 0:
            print("Saved until idx:" + str(idx + idx_correction))
            tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Covid\\"
                              r"Comments\submission_id_to_comments_dict"
                              + str(idx + idx_correction), submission_id_to_comments_dict)
            submission_id_to_comments_dict = dict()
        comment_list = list()
        try:
            submission = reddit.submission(sub_record["id"])
        except Forbidden as f_error:
            print(f_error)
        # submission.comments.replace_more(limit=None, threshold=0)
        for comment in submission.comments.list():
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
    # tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Twitter_Parser\I_O\Politics\\"
    #                   r"January 6 United States Capitol attack\submission_id_to_comments_dict",
    #                   submission_id_to_comments_dict)

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


if __name__ == "__main__":
    # getPushshiftData()
    # get_post_with_id()
    # get_submissions_records_for_time_range("2020-12-01", "2021-01-01", "health", "covid")
    # retrieve_comments_ids_per_submission()
    a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Covid\r_health_submission_records")
    print()

