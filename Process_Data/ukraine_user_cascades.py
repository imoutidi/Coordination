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


def create_submission_index():

    all_submissions = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                                        r"New_Submissions\worldnews_subs_2022-01-01_2023-04-01")
    submissions_index = dict()
    for sub in all_submissions:
        submissions_index[sub["id"]] = sub
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                      r"Indexes\submissions_index", submissions_index)


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
                                       r"Ukraine_War\Indexes\new_ukraine_comments_index")
    submission_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                                         r"Indexes\submissions_index")
    opinion_changed_comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                 r"Ukraine_War\Annotations\new_kept_comments")
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
        target_comment_id = comment_group[0]["comment_id"]
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
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
                      r"Annotations\new_populated_opinion_change_comments_with_parents_children_and_submission_post",
                      populated_with_parents)


def write_permalinks():
    comments = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\Annotations\\"
                                 r"For_Opinion_Change_Dataset\only_the_opinion_change_comment")
    with open(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\\"
              r"Annotations\For_Opinion_Change_Dataset\opinion_change_permalinks.html", "w") as out_file:
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
    ids_of_checked_comments = [0, 2, 3, 4, 6, 9, 10, 13, 16, 17, 19, 20, 22, 24, 25, 26, 28, 29, 30, 31, 34, 35, 36, 37,
                               38, 39, 40, 41, 42, 51, 53, 54, 55, 56, 58, 63, 64, 65, 68, 73, 75, 76, 77, 78, 79, 80,
                               81, 82, 84, 87, 89, 90, 91, 93, 94, 95, 96, 97, 102, 103, 104, 106, 109, 110, 112, 113,
                               115, 116, 118, 119, 121, 124, 125, 126, 127, 128, 129, 132, 134, 135, 139, 140, 141, 142,
                               143, 144, 146, 147, 148, 149, 150, 151, 153, 154, 155, 156, 158, 160, 162, 163, 164, 165,
                               166, 168, 171, 174, 175, 176, 177, 178, 179, 180, 184, 185, 187, 189, 192, 194, 195, 197,
                               198, 199, 204, 205, 207, 210, 211, 213, 216, 217, 218, 219, 220, 221, 222, 223, 228, 229,
                               231, 232, 238, 239, 240, 241, 243, 245, 251, 253, 254, 255, 256, 257, 259, 260, 261, 263,
                               264, 265, 266, 267, 268, 269, 271, 272, 273, 275, 276, 277, 278, 279, 282, 286, 287, 289,
                               290, 291, 292, 294, 295, 296, 297, 302, 304, 307, 310, 314, 315, 316, 317, 319, 320, 322,
                               323, 324, 326, 327, 328, 330, 331, 333, 335, 338, 339, 342, 345, 348, 350, 352, 354, 356,
                               357, 360, 361, 367, 368, 370, 372, 376, 377, 378, 380, 381, 384, 387, 389, 397, 398, 400,
                               401, 404, 405, 407, 410, 411, 412, 413, 414, 417, 419, 420, 422, 424, 425, 426, 428, 436,
                               437, 438, 439, 440, 442, 443, 446, 447, 449, 450, 453, 454, 455, 456, 457, 458, 459, 460,
                               464, 465, 466, 467, 470, 471, 472, 475, 477, 479, 482, 483, 484, 486, 487, 496, 497, 498,
                               499, 500, 501, 502, 505, 506, 507, 508, 509, 510, 511, 512, 513, 515, 516, 517, 518, 519,
                               520, 522, 524, 527, 528, 529, 530, 532, 533, 535, 536, 537, 538, 539, 542, 546, 547, 549,
                               550, 552, 553, 555, 557, 558, 559, 560, 561, 562, 563, 567, 568, 569, 571, 573, 574, 576,
                               578, 579, 580, 581, 582, 583, 584, 586, 587, 589, 590, 591, 592, 595, 596, 598, 599, 600,
                               603, 605, 606, 610, 611, 612, 615, 616, 618, 619, 620, 621, 624, 627, 629, 631, 634, 636,
                               638, 639, 644]
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
    annotate()
    # group_opinion_changed_with_parent_child_comments()
    # write_permalinks()
    # keep_checked_opinion_change_comments()
    # a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\Annotations\crypto_kept_comments")
    # b = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Crypto_Currency\Annotations\crypto_comment_number")

    print()
