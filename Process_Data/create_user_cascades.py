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

# I KNOW ABOUT THE NUMBERS
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
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Storm_on_capitol\Indexes\comments_index_with_irrelevant"
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
            snapshot_dict = {"author": author, "author_fullname": author_fullname, "id": sid, "title": title,
                             "selftext": selftext, "subreddit": subreddit, "timestamp": timestamp, "score": score}

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
                c_snapshot_dict = {"author": c_author, "author_fullname": c_author_fullname, "comment_id": c_sid,
                                   "post_id": sid, "body": c_body, "subreddit": c_subreddit, "timestamp": c_timestamp,
                                   "score": c_score, "parent_id": c_parent_id, "permalink": c_perma}
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


def create_submission_index():
    submissions_path = r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\" \
                       r"Storm_on_capitol\Merged_Submissions_Comments\\"
    submissions_index = dict()
    for idx, sub_file in enumerate(os.listdir(submissions_path)):
        print(idx)
        all_submissions = tools.load_pickle(submissions_path + sub_file)
        for sub in all_submissions:
            submissions_index[sub[0]["id"]] = sub
        tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                          r"Storm_on_capitol\Indexes\submissions_index", submissions_index)


def check_for_agreement_keywords():
    posts_per_user = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                                       r"Datasets\Storm_on_capitol\Indexes\posts_per_user_merged")
    key_phrase_to_opinion_comment = defaultdict(list)
    user_cascades = list()
    cascades_username_tracker = set()
    frequent_users_with_posts = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                                                  r"Datasets\Storm_on_capitol\Users\frequent_users_and_their_posts")
    submission_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                         r"Storm_on_capitol\Indexes\submissions_index")
    # agreement_key_phrases = ["i agree", "you were right", "you are right", "you're right", "thats true", "that is true",
    #                          "good point", "fair enough", "fair point", "you have a point", "you got a point",
    #                          "excellent point", "excellent argument", "good argument", "exactly this", " +1 ",
    #                          "ok got it", "got it", "i get it", "amen to that", "i see your point", "my bad",
    #                          "i am wrong", "i'm wrong", "i was wrong", "i went wrong", "you’re correct",
    #                          "you are correct", "i stand corrected"]
    against_trump_key_phrases = ["i used to support trump but ", "i used to like trump ", " i voted for trump ",
                                 "not voting for trump again ", " never again voting for trump ", " trump never again ",
                                 " changed my mind about trump ", " i don't like trump anymore ",
                                 " i was wrong voting for trump ", " changed my mind about trump ",
                                 " don't support trump anymore ", " i am disappointed on trump ",
                                 " i was wrong about trump ", " changed my view on trump ", " wrong on trump "]
    for f_user_tuple in frequent_users_with_posts:
        for u_post in f_user_tuple[1]:
            # body means it is a comment.
            if "body" in u_post:
                post_text = u_post["body"].lower().replace("\n", "").strip()
                for agree_phrase in against_trump_key_phrases:
                    if agree_phrase in post_text:
                        # temp_agreeable_posts.append((f_user_tuple[0][0], u_post))
                        key_phrase_to_opinion_comment[agree_phrase].append((f_user_tuple[0][0], u_post))
                        print(post_text)
                        print()
    for key_phrase, list_of_comments in key_phrase_to_opinion_comment.items():
        for agree_comment in list_of_comments:
            agree_user_cascade = posts_per_user[agree_comment[0]]
            for idx, user_comment in enumerate(agree_user_cascade):
                if agree_comment[1]["timestamp"] == user_comment["timestamp"]:
                    if "key_phrase" in user_comment:
                        user_comment["key_phrase"].append(key_phrase)
                    else:
                        user_comment["key_phrase"] = [key_phrase]
                    user_comment["post_comments"] = submission_index[user_comment["post_id"]]
            if agree_user_cascade[0]["author"] not in cascades_username_tracker:
                cascades_username_tracker.add(agree_user_cascade[0]["author"])
                user_cascades.append(agree_user_cascade)
    # indexing the comments in the users cascade where their text includes one or more "agree" key_phrases
    all_users_agree_indexes = list()
    for user_casc in user_cascades:
        indexes_list = list()
        for idx, casc_dict in enumerate(user_casc):
            if "post_comments" in casc_dict:
                indexes_list.append(idx)
        all_users_agree_indexes.append(indexes_list)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Storm_on_capitol\Users\anti_trump_user_cascades", user_cascades)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Storm_on_capitol\Users\all_anti_trump_users_indexes", all_users_agree_indexes)


def check_stuff():
    comments_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                       r"Storm_on_capitol\Indexes\comments_index")
    total_count = 0
    t1_count = 0
    t2_count = 0
    t3_count = 0
    for comment, comment_info in comments_index.items():
        total_count += 1
        if comment_info["parent_id"][0:3] == "t1_":
            t1_count += 1
        if comment_info["parent_id"][0:3] == "t2_":
            t2_count += 1
        if comment_info["parent_id"][0:3] == "t3_":
            t3_count += 1
        # print(comment_info["parent_id"])
    print(len(comments_index))
    print(f"total_count = {total_count}\n t1 = {t1_count} \n t2 = {t2_count} \n t3 = {t3_count}")


def annotate():
    comment_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                                      r"Datasets\Storm_on_capitol\Annotations\comment_number")
    comment_index = 0
    index_counter = 0
    agree_user_cascades = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                            r"Storm_on_capitol\Users\anti_trump_user_cascades")
    all_users_agree_indexes = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                r"Storm_on_capitol\Users\all_anti_trump_users_indexes")
    comments_with_agree_key_phrase = list()
    for user_cascade, index_list in zip(agree_user_cascades, all_users_agree_indexes):
        for c_index in index_list:
            comments_with_agree_key_phrase.append(user_cascade[c_index])
    comments_to_keep = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                                         r"Datasets\Storm_on_capitol\Annotations\kept_comments")
    comments_to_keep = list()
    for idx, comment in enumerate(comments_with_agree_key_phrase[comment_index:]):
        print_with_phrase_colored(comment["body"])
        # print(comment["body"])
        print(idx+comment_index)
        index_counter += 1
        answer = input("Keep this comment?")
        if answer == "Y":
            comments_to_keep.append(comment)
        if answer == "STOP":
            break
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                      r"Datasets\Storm_on_capitol\Annotations\kept_comments", comments_to_keep)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\\"
                      r"Datasets\Storm_on_capitol\Annotations\comment_number", comment_index + index_counter - 1)


def print_with_phrase_colored(in_str):
    colorama.init()
    agreement_key_phrases = ["i agree", "you were right", "you are right", "you're right", "thats true", "that is true",
                             "good point", "fair enough", "fair point", "you have a point", "you got a point",
                             "excellent point", "excellent argument", "good argument", "exactly this", " +1 ",
                             "ok got it", "got it", "i get it", "amen to that", "i see your point", "my bad",
                             "i am wrong", "i'm wrong", "i was wrong", "i went wrong", "you’re correct",
                             "you are correct", "i stand corrected"]

    for key_phrase in agreement_key_phrases:
        substring_index = in_str.lower().find(key_phrase)
        # print()
        if substring_index != -1:
            # The weird print is how colorama works.
            print(in_str[:substring_index] +
                  f"{Fore.GREEN}" +
                  in_str[substring_index:substring_index + len(key_phrase)] +
                  f"{Style.RESET_ALL}" +
                  in_str[substring_index + len(key_phrase):])


def opinion_changed():
    list_of_changed_ids = [6, 37, 62, 70, 85, 89, 93, 97, 100, 182, 183, 200, 201, 208, 222, 225, 241, 262, 263, 297,
                           339, 359, 360, 385, 386, 389, 430, 453, 422, 458, 470, 474, 477, 484, 486, 497, 501, 508,
                           514, 518, 524, 544, 554, 555, 570, 572, 600, 620, 626, 630, 631, 632, 633, 642, 653, 661,
                           676, 679, 700, 703, 715, 717, 721, 724, 735, 736, 739, 752, 758, 759, 762, 782, 784, 792,
                           795, 828, 836, 839, 841, 850, 853, 874, 891, 892, 915, 916, 918, 943, 944, 957, 973, 1020,
                           1022, 1023, 1055, 1056, 1064, 1065, 1073, 1104, 1142, 1174, 1175, 1176, 1184, 1224, 1244,
                           1246, 1260, 1272, 1312, 1335, 1373, 1376, 1410, 1411, 1427, 1434, 1435, 1436, 1453, 1463,
                           1473, 1525, 1559, 1569, 1602, 1615, 1643, 1654, 1655, 1677, 1681, 1683, 1685, 1725, 1765,
                           1766, 1791, 1792, 1796, 1798, 1835, 1873, 1877, 1886, 1895, 1897, 1902, 1905, 1910, 1927,
                           1933, 1945, 1946, 1958, 1980, 1997, 2013, 2018, 2021, 2022, 2030, 2039, 2121, 2122, 2128,
                           2132, 2144, 2195, 2231, 2241, 2286, 2301, 2319, 2379, 2383, 2406, 2409, 2412, 2413, 2415,
                           2426, 2459, 2462, 2463, 2464, 2465, 2467, 2470, 2471, 2475, 2483, 2485, 2488, 2489, 2490,
                           2493, 2494, 2497, 2498, 2499, 2500, 2501, 2502, 2507, 2508, 2509, 2510, 2511, 2513, 2515,
                           2519, 2520, 2521, 2522, 2524, 2525, 2528, 2530, 2531, 2532, 2536, 2537, 2538, 2539, 2545,
                           2552, 2557, 2576, 2580, 2583, 2587, 2589, 2590, 2595, 2598, 2603, 2605, 2606, 2607, 2608,
                           2609, 2611, 2622, 2624, 2637, 2647, 2654, 2657, 2666, 2672, 2679, 2761, 2768, 2769, 2774,
                           2796, 2797, 2806, 2809, 2810, 2811, 2817, 2829]

    second_pick_indexes = [1, 3, 5, 6, 8, 9, 10, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 35,
                           36, 37, 38, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 54, 55, 60, 61, 62, 64, 66, 68, 69, 70,
                           71, 72, 73, 74, 75, 76, 77, 82, 83, 85, 86, 87, 88, 89, 90, 91, 93, 94, 95, 96, 97, 99, 101,
                           102, 103, 104, 107, 108, 109, 110, 112, 114, 115, 116, 117, 119, 121, 123, 124, 127, 128,
                           133, 134, 135, 141, 142, 143, 144, 145, 147, 148, 149, 150, 152, 153, 154, 156, 157, 158,
                           159, 160, 161, 162, 164, 165, 166, 168, 172, 173, 174, 176, 177, 178, 179, 180, 182, 183,
                           184, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 200, 202, 205, 206, 208,
                           209, 210, 211, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 224, 227, 230, 231, 232,
                           233, 234, 236, 238, 239, 240, 241, 242, 243, 244, 245, 246, 248, 249, 251, 252, 253, 254,
                           255, 256, 258, 259, 260, 261, 263, 264]

    agree_user_cascades = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                            r"Storm_on_capitol\Users\agree_user_cascades")
    all_users_agree_indexes = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                r"Storm_on_capitol\Users\all_users_agree_indexes")
    comments_with_agree_key_phrase = list()
    for user_cascade, index_list in zip(agree_user_cascades, all_users_agree_indexes):
        for c_index in index_list:
            comments_with_agree_key_phrase.append(user_cascade[c_index])

    # Gather the permalinks in a file, add the prefix https://www.reddit.com/ as well.
    permalink_list = list()
    for idx in second_pick_indexes:
        permalink_list.append("https://www.reddit.com" + comments_with_agree_key_phrase[list_of_changed_ids[idx]]["permalink"])
    with open(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\\"
              r"Annotations\opinion_change_permalinks.html", "w") as perma_file:
        for idx, url in enumerate(permalink_list):
            # perma_file.write(url + "\n")
            perma_file.write(str(idx) + " <a href=" + url + ">" + url + "</a><br>")


def group_opinion_changed_with_parent_child_comments():
    list_of_changed_ids = [6, 37, 62, 70, 85, 89, 93, 97, 100, 182, 183, 200, 201, 208, 222, 225, 241, 262, 263, 297,
                           339, 359, 360, 385, 386, 389, 430, 453, 422, 458, 470, 474, 477, 484, 486, 497, 501, 508,
                           514, 518, 524, 544, 554, 555, 570, 572, 600, 620, 626, 630, 631, 632, 633, 642, 653, 661,
                           676, 679, 700, 703, 715, 717, 721, 724, 735, 736, 739, 752, 758, 759, 762, 782, 784, 792,
                           795, 828, 836, 839, 841, 850, 853, 874, 891, 892, 915, 916, 918, 943, 944, 957, 973, 1020,
                           1022, 1023, 1055, 1056, 1064, 1065, 1073, 1104, 1142, 1174, 1175, 1176, 1184, 1224, 1244,
                           1246, 1260, 1272, 1312, 1335, 1373, 1376, 1410, 1411, 1427, 1434, 1435, 1436, 1453, 1463,
                           1473, 1525, 1559, 1569, 1602, 1615, 1643, 1654, 1655, 1677, 1681, 1683, 1685, 1725, 1765,
                           1766, 1791, 1792, 1796, 1798, 1835, 1873, 1877, 1886, 1895, 1897, 1902, 1905, 1910, 1927,
                           1933, 1945, 1946, 1958, 1980, 1997, 2013, 2018, 2021, 2022, 2030, 2039, 2121, 2122, 2128,
                           2132, 2144, 2195, 2231, 2241, 2286, 2301, 2319, 2379, 2383, 2406, 2409, 2412, 2413, 2415,
                           2426, 2459, 2462, 2463, 2464, 2465, 2467, 2470, 2471, 2475, 2483, 2485, 2488, 2489, 2490,
                           2493, 2494, 2497, 2498, 2499, 2500, 2501, 2502, 2507, 2508, 2509, 2510, 2511, 2513, 2515,
                           2519, 2520, 2521, 2522, 2524, 2525, 2528, 2530, 2531, 2532, 2536, 2537, 2538, 2539, 2545,
                           2552, 2557, 2576, 2580, 2583, 2587, 2589, 2590, 2595, 2598, 2603, 2605, 2606, 2607, 2608,
                           2609, 2611, 2622, 2624, 2637, 2647, 2654, 2657, 2666, 2672, 2679, 2761, 2768, 2769, 2774,
                           2796, 2797, 2806, 2809, 2810, 2811, 2817, 2829]

    second_pick_indexes = [1, 3, 5, 6, 8, 9, 10, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 35,
                           36, 37, 38, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 54, 55, 60, 61, 62, 64, 66, 68, 69, 70,
                           71, 72, 73, 74, 75, 76, 77, 82, 83, 85, 86, 87, 88, 89, 90, 91, 93, 94, 95, 96, 97, 99, 101,
                           102, 103, 104, 107, 108, 109, 110, 112, 114, 115, 116, 117, 119, 121, 123, 124, 127, 128,
                           133, 134, 135, 141, 142, 143, 144, 145, 147, 148, 149, 150, 152, 153, 154, 156, 157, 158,
                           159, 160, 161, 162, 164, 165, 166, 168, 172, 173, 174, 176, 177, 178, 179, 180, 182, 183,
                           184, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 200, 202, 205, 206, 208,
                           209, 210, 211, 212, 213, 214, 215, 217, 219, 220, 221, 222, 223, 224, 227, 230, 231, 232,
                           233, 234, 236, 238, 239, 240, 241, 242, 243, 244, 245, 246, 248, 249, 251, 252, 253, 254,
                           255, 256, 258, 259, 260, 261, 263, 264]
    comments_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                       r"Storm_on_capitol\Indexes\comments_index_with_irrelevant")
    submissions_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                          r"Storm_on_capitol\Indexes\submissions_index")
    agree_user_cascades = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                            r"Storm_on_capitol\Users\agree_user_cascades")
    all_users_agree_indexes = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                                r"Storm_on_capitol\Users\all_users_agree_indexes")
    comments_with_agree_key_phrase = list()
    for user_cascade, index_list in zip(agree_user_cascades, all_users_agree_indexes):
        for c_index in index_list:
            comments_with_agree_key_phrase.append(user_cascade[c_index])

    all_populated_comments_with_parents = list()
    ids_not_found = 0
    # for idx in list_of_changed_ids:
    for idx in second_pick_indexes:
        list_of_submission_parent_and_original_comments = list()
        comment_meta = comments_with_agree_key_phrase[list_of_changed_ids[idx]]
        submission_meta = submissions_index[comment_meta["post_id"]]
        # Appending the agreement comment
        list_of_submission_parent_and_original_comments.append(comment_meta)
        parent_post_kind = comment_meta["parent_id"][0:2]
        parent_post_id = comment_meta["parent_id"][3:]
        # Appending the parent comments
        while parent_post_kind == "t1":
            if parent_post_id in comments_index:
                comment_meta = comments_index[parent_post_id]
                comment_meta["comment_id"] = parent_post_id
                list_of_submission_parent_and_original_comments.append(comment_meta)
                parent_post_kind = comment_meta["parent_id"][0:2]
                parent_post_id = comment_meta["parent_id"][3:]
            else:
                parent_post_kind = "exit"
                ids_not_found += 1
        # Appending the submission post
        list_of_submission_parent_and_original_comments.append(submission_meta[0])
        all_populated_comments_with_parents.append(list_of_submission_parent_and_original_comments)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\\"
                      r"Annotations\populated_opinion_change_comments_with_parents_and_submission_post",
                      all_populated_comments_with_parents)
    print(ids_not_found)
    # with open(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\Annotations\\"
    #           r"populated_agree_comments_with_parents.txt", "w", encoding='utf-8') as parents_file:
    #     for idx, parent_list in enumerate(all_populated_comments_with_parents):
    #         parents_file.write("Comment: " + str(idx) + "\n")
    #         submission_data = parent_list.pop()
    #         parents_file.write("Author: " + submission_data["author"] + " Post ID: " + submission_data["id"] +
    #                            "\nTitle: " + submission_data["title"] +
    #                            " Selftext: " + submission_data["selftext"] + "\n\n")
    #         for meta_data in reversed(parent_list):
    #             print()
    #             parents_file.write("Author: " + meta_data["author"] + " Comment_ID: " + meta_data["comment_id"] +
    #                                "\n" + "Body: " + meta_data["body"] + "\n\n")
    #         parents_file.write("\n")


def populate_opinion_change_comments_with_child_comments():
    submission_and_parents = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                               r"Storm_on_capitol\Annotations\\"
                                               r"populated_opinion_change_comments_with_parents_and_submission_post")
    submissions_index = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                          r"Storm_on_capitol\Indexes\submissions_index")
    # The opinion change comment is always the first for each list of comments in the submission and parents pickle.
    # The submission is always the last on the list.
    # The children of the opinion change comment will be added after the submission post.
    for opinion_ch in submission_and_parents:
        submission_id = opinion_ch[-1]["id"]
        target_comment_id = opinion_ch[0]["comment_id"]
        submission_comments = submissions_index[submission_id][1]

        for comment in submission_comments:
            if target_comment_id in comment["parent_id"]:
                if comment["author_fullname"] == "N_A":
                    c_author = "N_A"
                    c_author_fullname = "N_A"
                    c_sid = comment["id"]
                    c_body = comment["body"]
                    c_subreddit = comment["subreddit"]
                    if comment["created_utc"] == "N_A":
                        c_timestamp = -1
                    else:
                        c_timestamp = int(comment["created_utc"])
                    c_score = comment["score"]
                    c_perma = comment["permalink"]
                    c_parent_id = comment["parent_id"]
                    c_snapshot_dict = {"author": c_author, "author_fullname": c_author_fullname,
                                       "post_id": submission_id, "body": c_body, "subreddit": c_subreddit,
                                       "timestamp": c_timestamp, "score": c_score, "parent_id": c_parent_id,
                                       "permalink": c_perma, "comment_id": c_sid, "is_child": True}
                    opinion_ch.append(c_snapshot_dict)
                    continue
                c_author = comment["author"].name
                c_author_fullname = comment["author_fullname"]
                c_sid = comment["id"]
                c_body = comment["body"]
                c_subreddit = comment["subreddit"]
                c_timestamp = int(comment["created_utc"])
                c_score = comment["score"]
                c_perma = comment["permalink"]
                c_parent_id = comment["parent_id"]
                c_snapshot_dict = {"author": c_author, "author_fullname": c_author_fullname, "post_id": submission_id,
                                   "body": c_body, "subreddit": c_subreddit, "timestamp": c_timestamp,
                                   "score": c_score, "parent_id": c_parent_id, "permalink": c_perma,
                                   "comment_id": c_sid, "is_child": True}
                opinion_ch.append(c_snapshot_dict)

    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Storm_on_capitol\Annotations\\"
                      r"populated_opinion_change_comments_with_parents_children_and_submission_post",
                      submission_and_parents)


def anti_trump():
    print()


if __name__ == "__main__":
    # merge_submissions_and_comments()
    # scan_users()
    # filter_users_on_number_of_posts()
    # create_comments_index()
    # check_stuff()
    # create_submission_index()
    # check_for_agreement_keywords()
    # annotate()
    # opinion_changed()
    # group_opinion_changed_with_parent_child_comments()
    # populate_opinion_change_comments_with_child_comments()

    #
    print()