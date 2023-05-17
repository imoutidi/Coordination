import os
import math
import goto

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
                                    r"New_Comments\worldnews_2022-01-01_2023-04-01")

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
                      r"Indexes\new_ukraine_comments_index", comments_dict)


def scan_for_agreement_phrases():
    key_phrase_to_opinion_comment = defaultdict(list)
    agreement_key_phrases = ["i agree", "you were right", "you are right", "you're right", "thats true", "that is true",
                             "good point", "fair enough", "fair point", "you have a point", "you got a point",
                             "excellent point", "excellent argument", "good argument", "exactly this", " +1 ",
                             "ok got it", "got it", "i get it", "amen to that", "i see your point", "my bad",
                             "i am wrong", "i'm wrong", "i was wrong", "i went wrong", "you’re correct",
                             "you are correct", "i stand corrected"]
    all_comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                     r"Ukraine_War\Indexes\new_ukraine_comments_index")
    for comment_id, comment_attrs in all_comments.items():
        post_text = comment_attrs["body"].lower().replace("\n", "").strip()
        for agree_phrase in agreement_key_phrases:
            if agree_phrase in post_text:
                comment_attrs["comment_id"] = comment_id
                key_phrase_to_opinion_comment[agree_phrase].append(comment_attrs)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Ukraine_War\Comments\New_Comments\agree_key_phrases", key_phrase_to_opinion_comment)


def annotate():
    comment_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                      r"Ukraine_War\Annotations\new_comment_number")
    # comment_index = 0
    index_counter = 0

    comments_to_keep = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                         r"Ukraine_War\Annotations\new_kept_comments")
    comments_with_agree_keyphrase = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                      r"Ukraine_War\Comments\New_Comments\agree_key_phrases")
    # comments_to_keep = list()
    merged_comment_list = list()
    for keyphrase, comment_list in comments_with_agree_keyphrase.items():
        merged_comment_list += comment_list

    for comment in merged_comment_list[comment_index:]:
        print(comment_index + index_counter)
        index_counter += 1
        if "i agree" in comment["body"].lower():
            continue
        print_with_phrase_colored(comment["body"])
        # print(comment["body"])
        answer = input("Keep this comment?")
        if answer == "Y":
            comments_to_keep.append(comment)
        if answer == "STOP":
            break

    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Ukraine_War\Annotations\new_kept_comments", comments_to_keep)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Ukraine_War\Annotations\new_comment_number", comment_index + index_counter - 1)


def print_with_phrase_colored(in_str):
    colorama.init()
    agreement_key_phrases = ["i agree", "you were right", "you are right", "you're right", "thats true", "that is true",
                             "good point", "fair enough", "fair point", "you have a point", "you got a point",
                             "excellent point", "excellent argument", "good argument", "exactly this", " +1 ",
                             "ok got it", "got it", "i get it", "amen to that", "i see your point", "my bad",
                             "i am wrong", "i'm wrong", "i was wrong", "i went wrong", "you’re correct",
                             "you are correct", "i stand corrected"]

    characters_per_line = 180
    words = in_str.split()
    in_str_with_linebreaks = ""
    current_line_length = 0

    for word in words:
        word_length = len(word)
        if current_line_length + word_length <= characters_per_line:
            in_str_with_linebreaks += word + " "
            current_line_length += word_length + 1
        else:
            in_str_with_linebreaks = in_str_with_linebreaks.rstrip() + "\n\n" + word + " "
            current_line_length = word_length + 1

    for key_phrase in agreement_key_phrases:
        substring_index = in_str_with_linebreaks.lower().find(key_phrase)
        # print()
        if substring_index != -1:
            # The weird print is how colorama works.
            print(in_str_with_linebreaks[:substring_index] +
                  f"{Fore.GREEN}" +
                  in_str_with_linebreaks[substring_index:substring_index + len(key_phrase)] +
                  f"{Style.RESET_ALL}" +
                  in_str_with_linebreaks[substring_index + len(key_phrase):])
            # this is for better posture
            print("\n\n\n\n\n\n\n\n\n\n\n\n")

def group_opinion_changed_with_parent_child_comments():
    comments_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                       r"Ukraine_War\Indexes\ukraine_comments_index")
    opinion_changed_comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                 r"Ukraine_War\Annotations\kept_comments")
    # populate with parent comments
    populated_with_parents = list()
    for comment_meta in opinion_changed_comments:
        group_of_comments = list()
        group_of_comments.append(comment_meta)
        parent_post_kind = comment_meta["parent_id"][0:2]
        parent_post_id = comment_meta["parent_id"][3:]
        while parent_post_kind == "t1":
            parent_comment = comments_index[parent_post_id]
            parent_comment["comment_id"] = parent_post_id
            group_of_comments.append(parent_comment)
            parent_post_kind = parent_comment["parent_id"][0:2]
            parent_post_id = parent_comment["parent_id"][3:]
        populated_with_parents.append(group_of_comments)
    # populate_with_child_comments
    for comment_group in populated_with_parents:
        target_comment_id = comment_group[0]["comment_id"]
        for comment_id, comment_meta in comments_index.items():
            if target_comment_id in comment_meta["parent_id"]:
                comment_meta["comment_id"] = comment_id
                comment_meta["is_child"] = True
                comment_group.append(comment_meta)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                      r"Annotations\populated_opinion_change_comments_with_parents_children_and_submission_post",
                      populated_with_parents)


def write_permalinks():
    comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                 r"Ukraine_War\Annotations\kept_comments")
    with open(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
              r"Annotations\ukraine_permalinks.html", "w") as out_file:
        for idx, comment in enumerate(comments):
            url = comment["permalink"]
            out_file.write(str(idx) + " <a href=" + url + ">" + url + "</a><br>")


def merge_submissions():
    merge_dict = dict()
    input_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\New_Comments\\"
    for filename in os.listdir(input_path):
        comments_per_submission = tools.load_pickle(input_path + filename)
        for sid, s_comments in comments_per_submission.items():
            merge_dict[sid] = s_comments

    tools.save_pickle(input_path + "worldnews_2022-01-01_2023-04-01", merge_dict)


if __name__ == "__main__":
    # create_comments_index()

    # scan_for_agreement_phrases()
    annotate()
    # group_nopinion_changed_with_parent_child_comments()
    # write_permalinks()
    # a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
    #                       r"Ukraine_War\Annotations\new_kept_comments")
    print()
