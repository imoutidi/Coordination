import os
from dateutil.relativedelta import relativedelta
from Tool_Pack import tools
from operator import itemgetter
from collections import defaultdict
import pandas as pd
import json
import csv
import time
import datetime


def merge_submissions_and_comments():
    comments_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\Comments\\"
    all_submissions = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                        r"Storm_on_capitol\submission_records")
    # convert submission file into a dictionary key = post id
    # I don't iterate the submission_list file because the comments are
    # divided in many pickle files.
    submission_dict = dict()
    for sub_record in all_submissions:
        submission_dict[sub_record["id"]] = sub_record
    # This will be a list of tuples
    for idx, comment_file in enumerate(os.listdir(comments_path)):
        print(idx)
        merged_subs_and_comments = list()
        current_comments = tools.load_pickle(comments_path + comment_file)
        for submission_id, comment_attributes in current_comments.items():
            merged_subs_and_comments.append((submission_dict[submission_id], comment_attributes))
        tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                          r"Storm_on_capitol\Merged_Submissions_Comments\subs_comments_"
                          + str(idx), merged_subs_and_comments)


def create_comments_index():
    list_of_irrelevant_usernames = ["t2_6l4z3", "t2_onl9u", "N_A"]
    records_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\" \
                   r"Storm_on_capitol\Merged_Submissions_Comments\\"
    comments_dict = dict()
    for idx, record_file in enumerate(os.listdir(records_path)):
        print(idx)
        all_records = tools.load_pickle(records_path + record_file)
        for current_record in all_records:
            sid = current_record[0]["id"]
            for post_comment in current_record[1]:
                if post_comment["author_fullname"] in list_of_irrelevant_usernames:
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
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Storm_on_capitol\Indexes\comments_index"
                      , comments_dict)


def scan_users():
    list_of_irrelevant_usernames = ["t2_6l4z3", "t2_onl9u", "N_A"]
    records_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\" \
                   r"Storm_on_capitol\Merged_Submissions_Comments\\"
    dictionary_of_usernames = dict()
    for idx, record_file in enumerate(os.listdir(records_path)):
        print(idx)
        all_records = tools.load_pickle(records_path + record_file)
        for current_record in all_records:
            author_fullname = current_record[0]["author_fullname"]
            author = str(current_record[0]["author"])
            sid = current_record[0]["id"]
            score = current_record[0]["score"]
            title = current_record[0]["title"]
            selftext = current_record[0]["selftext"]
            subreddit = current_record[0]["subreddit"]
            timestamp = tools.str_datetime_to_timestamp(current_record[0]["utc_datetime_str"])
            snapshot_dict = {"author": author, "id": sid, "title": title, "selftext": selftext,
                             "subreddit": subreddit, "timestamp": timestamp, "score": score}

            if author_fullname in dictionary_of_usernames:
                dictionary_of_usernames[author_fullname].append(snapshot_dict)
            else:
                dictionary_of_usernames[author_fullname] = list()
                dictionary_of_usernames[author_fullname].append(snapshot_dict)
            for post_comment in current_record[1]:
                if post_comment["author_fullname"] in list_of_irrelevant_usernames:
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
                c_snapshot_dict = {"author": c_author, "comment_id": c_sid, "post_id": sid, "body": c_body,
                                   "subreddit": c_subreddit, "timestamp": c_timestamp, "score": c_score,
                                   "parent_id": c_parent_id, "permalink": c_perma}
                if c_author_fullname in dictionary_of_usernames:
                    dictionary_of_usernames[c_author_fullname].append(c_snapshot_dict)
                else:
                    dictionary_of_usernames[c_author_fullname] = list()
                    dictionary_of_usernames[c_author_fullname].append(c_snapshot_dict)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Storm_on_capitol\Indexes\posts_per_user_merged"
                      , dictionary_of_usernames)


def filter_users_on_number_of_posts():
    users_dict = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\\"
                                   r"Indexes\posts_per_user_merged")
    users_posts_list = list()
    for user_id in users_dict:
        users_posts_list.append((user_id, len(users_dict[user_id])))
    users_posts_sorted = sorted(users_posts_list, key=itemgetter(1), reverse=True)
    del users_posts_sorted[0]
    frequent_posters = list()
    for user_tuple in users_posts_sorted:
        if user_tuple[1] > 20:
            frequent_posters.append(user_tuple)
    # for each frequent user get his posts and sort them based on their timestamp, older to newer.
    frequent_users_with_posts = list()
    for frequent_user in frequent_posters:
        sorted_user_posts = users_dict[frequent_user[0]]
        sorted_user_posts = sorted(sorted_user_posts, key=itemgetter("timestamp"))
        frequent_users_with_posts.append((frequent_user, sorted_user_posts))
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                      r"Datasets\Storm_on_capitol\Users\frequent_users_and_their_posts", frequent_users_with_posts)


def check_for_agreement_keywords():
    key_phrase_to_opinion_comment = defaultdict(list)
    frequent_users_with_posts = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                                                  r"Datasets\Storm_on_capitol\Users\frequent_users_and_their_posts")
    comments_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                       r"Storm_on_capitol\Indexes\comments_index")
    agreement_key_phrases = ["i agree", "you were right", "you are right", "thats true", "that is true", "good point",
                             "fair enough", "fair point", "you have a point", "you got a point", "excellent point",
                             "excellent argument", "good argument", "exactly this", " +1 ", "ok got it", "got it",
                             "i get it", "amen to that", "i see your point", "my bad", "i was wrong", "i went wrong",
                             "you’re correct", "you are correct", "i stand corrected"]
    for f_user_tuple in frequent_users_with_posts:
        for u_post in f_user_tuple[1]:
            if "body" in u_post:
                post_text = u_post["body"].lower().replace("\n", "").strip()
                for agree_phrase in agreement_key_phrases:
                    if agree_phrase in post_text:
                        # temp_agreeable_posts.append((f_user_tuple[0][0], u_post))
                        key_phrase_to_opinion_comment[agree_phrase].append((f_user_tuple[0][0], u_post))

                        # we get duplicates otherwise.
                        # break
    print()


if __name__ == "__main__":
    # merge_submissions_and_comments()
    # scan_users()
    # filter_users_on_number_of_posts()
    # create_comments_index()
    check_for_agreement_keywords()
    # a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\Indexes\comments_index")
    print()