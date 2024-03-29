import os
import math
import goto
from sklearn.neighbors import NearestNeighbors

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


def create_submission_index():

    all_submissions = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                                        r"New_Submissions\merged_submissions")
    submissions_index = dict()
    for sub in all_submissions:
        submissions_index[sub["id"]] = sub
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                      r"Indexes\submissions_index", submissions_index)


def create_comments_index():
    comments_dict = dict()
    all_records = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                                    r"Comments\all_comments")
    print()
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
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                      r"Indexes\comments_index", comments_dict)


def scan_for_agreement_phrases():
    key_phrase_to_opinion_comment = defaultdict(list)
    agreement_key_phrases = ["i agree", "you were right", "you are right", "you're right", "thats true", "that is true",
                             "good point", "fair enough", "fair point", "you have a point", "you got a point",
                             "excellent point", "excellent argument", "good argument", "exactly this", " +1 ",
                             "ok got it", "got it", "i get it", "amen to that", "i see your point", "my bad",
                             "i am wrong", "i'm wrong", "i was wrong", "i went wrong", "you’re correct",
                             "you are correct", "i stand corrected"]
    all_comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                                     r"Comments\all_comments")
    for submission_id, comment_attrs in all_comments.items():
        for comment in comment_attrs:
            post_text = comment["body"].lower().replace("\n", "").strip()
            for agree_phrase in agreement_key_phrases:
                if agree_phrase in post_text:
                    comment["submission_id"] = submission_id
                    key_phrase_to_opinion_comment[agree_phrase].append(comment)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\Comments\\"
                      r"agree_comments", key_phrase_to_opinion_comment)


def annotate():
    # Load the index of the comment when we stopped last time
    comment_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                                      r"Annotations\crypto_comment_number")

    # The first time use this line.
    # comment_index = 0
    index_counter = 0

    # comments_to_keep = list()
    comments_to_keep = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                                         r"Annotations\crypto_kept_comments")
    comments_with_agree_keyphrase = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                      r"Crypto_Currency\Comments\agree_comments")
    # comments_to_keep = list()
    merged_comment_list = list()
    for keyphrase, comment_list in comments_with_agree_keyphrase.items():
        print()
        merged_comment_list += comment_list

    for comment in merged_comment_list[comment_index:]:
        print(comment_index + index_counter)
        index_counter += 1
        # if "i agree" in comment["body"].lower():
        #     continue
        print_with_phrase_colored(comment["body"])
        # print(comment["body"])
        answer = input("Keep this comment?")
        if answer == "Y":
            comments_to_keep.append(comment)
        if answer == "STOP":
            break

    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                      r"Annotations\crypto_kept_comments", comments_to_keep)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                      r"Annotations\crypto_comment_number", comment_index + index_counter - 1)


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
                                       r"Crypto_Currency\Indexes\comments_index")
    submission_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                         r"Crypto_Currency\Indexes\submissions_index")
    opinion_changed_comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                 r"Crypto_Currency\Annotations\crypto_kept_comments")
    print()
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
        target_comment_id = comment_group[0]["id"]
        for comment_id, comment_meta in comments_index.items():
            if target_comment_id in comment_meta["parent_id"]:
                comment_meta["comment_id"] = comment_id
                comment_meta["is_child"] = True
                comment_group.append(comment_meta)
    print()
    # populate with submissions
    for comment_group in populated_with_parents:
        for comment in comment_group:
            parent_post_kind = comment["parent_id"][0:2]
            parent_post_id = comment["parent_id"][3:]
            if parent_post_kind == "t3":
                # if parent_post_id in submission_index:
                submission = submission_index[parent_post_id]
                comment_group.append(submission)
                break
    print()
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\Annotations\\"
                      r"new_populated_opinion_change_comments_with_parents_children_and_submission_post",
                      populated_with_parents)


def write_permalinks():
    comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\"
                                 r"Annotations\crypto_kept_comments")
    with open(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\Annotations\\"
              r"For_Opinion_Change_Dataset\opinion_change_permalinks.html", "w") as out_file:
        out_file.write("<!DOCTYPE html>\n<html>\n<head>\n \t <base href=\"https://www.reddit.com/\"/>\n</head>\n<body>\n")
        for idx, comment in enumerate(comments):
            url = comment["permalink"]
            out_file.write(str(idx) + " <a href=" + url + ">" + url + "</a><br>\n")
        out_file.write("</body>\n</html>")


def merge_submissions():
    all_submissions = list()
    input_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\New_Submissions\\"
    for filename in os.listdir(input_path):
        submissions = tools.load_pickle(input_path + filename)
        for sub in submissions:
            all_submissions.append(sub)

    tools.save_pickle(input_path + "worldnews_subs_2022-01-01_2023-04-01", all_submissions)


def keep_checked_opinion_change_comments():
    ids_of_checked_comments = [1, 2, 4, 14, 17, 19, 20, 21, 25, 28, 29, 31, 33, 35, 41, 45, 49, 51, 62, 63, 66, 67, 78,
                               86, 94, 96, 100, 101, 102, 103, 106, 107, 108, 110, 112, 113, 119, 121, 123, 125, 126,
                               128, 133, 134, 135, 138, 139, 140, 141, 146, 148, 150, 152, 153, 156, 158, 160, 162, 165,
                               168, 170, 174, 176, 177, 178, 181, 183, 185, 193, 196, 200, 203, 211, 224, 253, 256, 270,
                               299, 306, 307, 309, 311, 314, 325, 326, 327, 328, 331, 332, 334, 341, 359, 361, 364, 366,
                               367, 372, 374, 380, 381, 382, 387, 392, 402, 403, 412, 418, 437, 458, 459, 463, 467, 471,
                               480, 489, 568, 576, 582, 586, 597, 602, 627, 653, 654, 661, 667, 668, 676, 685, 689, 693,
                               698, 710, 717, 728, 732, 734, 739, 744, 755, 779, 781, 788, 789, 791, 795, 797, 798, 799,
                               808, 820, 821, 824, 825, 842, 845, 847, 853, 855, 856, 857, 859, 860, 861, 862, 863, 865,
                               866, 867, 868, 873, 874, 875, 876, 878, 881, 882, 889, 890, 891, 893, 899, 913]
    children_parents = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                                         r"Annotations\new_populated_opinion_change_comments_with_parents_children_and_submission_post")
    children_parents_small = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                                               r"Annotations\populated_opinion_change_comments_with_parents_children_and_submission_post")
    kept = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\Annotations\kept_comments")
    new_kept = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\Annotations\new_kept_comments")
    opinion_change_kept = list()
    populated_opinion_change = list()
    for idx in ids_of_checked_comments:
        populated_opinion_change.append(children_parents[idx])
        opinion_change_kept.append(new_kept[idx])
    for comment_group in children_parents_small:
        populated_opinion_change.append(comment_group)
    opinion_change_kept += kept
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\Annotations\\"
                      r"For_Opinion_Change_Dataset\populated_opinion_change_ukraine", populated_opinion_change)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\Annotations\\"
                      r"For_Opinion_Change_Dataset\only_the_opinion_change_comment", opinion_change_kept)


if __name__ == "__main__":
    # create_comments_index()
    # create_submission_index()
    # merge_submissnions()
    # scan_for_agreement_phrases()
    # annotate()
    # group_opinion_changed_with_parent_child_comments()
    write_permalinks()
    # keep_checked_opinion_change_comments()
    # a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\Annotations\\"
    #                       r"new_populated_opinion_change_comments_with_parents_children_and_submission_post")
    # b = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\\
    # Annotations\crypto_kept_comments")
    print()
