import os

import colorama
from dateutil.relativedelta import relativedelta
from Tool_Pack import tools
from operator import itemgetter
from collections import defaultdict
import pandas as pd
import json
import csv
import time
import datetime

# Display colored text in console
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


def create_comments_index():
    comments_dict = dict()
    all_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                                    r"Comments\submission_id_to_comments_tjcwy9")

    for current_record, submission_comments in all_records.items():
        sid = current_record
        for post_comment in submission_comments:
            if post_comment["author_fullname"] == "N_A":
                c_author = "N_A"
                c_author_fullname = "N_A"
                c_sid = post_comment["id"]
                c_body = post_comment["body"]
                c_subreddit = post_comment["subreddit"]
                if post_comment["created_utc"] == "N_A":
                    c_timestamp = -1
                else:
                    c_timestamp = int(post_comment["created_utc"])
                c_score = post_comment["score"]
                c_perma = post_comment["permalink"]
                c_parent_id = post_comment["parent_id"]
                c_snapshot_dict = {"author": c_author, "author_fullname": c_author_fullname, "post_id": sid,
                                   "body": c_body, "subreddit": c_subreddit, "timestamp": c_timestamp,
                                   "score": c_score, "parent_id": c_parent_id, "permalink": c_perma}
                comments_dict[c_sid] = c_snapshot_dict
                continue
            c_author = post_comment["author"].name
            c_author_fullname = post_comment["author_fullname"]
            c_sid = post_comment["id"]
            c_body = post_comment["body"]
            c_subreddit = post_comment["subreddit"]
            c_timestamp = int(post_comment["created_utc"])
            c_score = post_comment["score"]
            c_perma = post_comment["permalink"]
            c_parent_id = post_comment["parent_id"]
            c_snapshot_dict = {"author": c_author, "author_fullname": c_author_fullname, "post_id": sid,
                               "body": c_body, "subreddit": c_subreddit, "timestamp": c_timestamp,
                               "score": c_score, "parent_id": c_parent_id, "permalink": c_perma}
            comments_dict[c_sid] = c_snapshot_dict
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                      r"Indexes\ukraine_comments_index", comments_dict)


def scan_for_agreement_phrases():
    all_comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                     r"Ukraine_War\Indexes\ukraine_comments_index")
    opinion_change_comments = list()
    for comment_id, comment_attrs in all_comments.items():
        if "my bad" in comment_attrs["body"]:
            opinion_change_comments.append(comment_id)
    print()


if __name__ == "__main__":
    # create_comments_index()
    scan_for_agreement_phrases()
    print()
