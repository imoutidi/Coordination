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
import r_scrapper


reddit = praw.Reddit(client_id="JA5vOF4gOhcjuGqdHU2Gcw", client_secret="3XT735o7Yc5dPql4EG9ThcqVgzrPZw",
                     user_agent="Climate_Change")


def crawl_megathreads(start_post_id="12aw2q2"):
    posts_id_list = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                                      r"Ukraine_War\all_megathreads_post_ids_temp")
    # start_post_id = "v0v1yv"
    while start_post_id is not None:
        current_post = r_scrapper.get_post_with_id(start_post_id)
        if current_post is None:
            print(f"Pushshift could not retrieve data for post {start_post_id}. Saving the post id list. \n"
                  f"need to find the next post id manually.")
            tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                              r"Ukraine_War\all_megathreads_post_ids_temp", posts_id_list)
            exit()

        post_text = current_post["selftext"]
        post_utc_timestamp = current_post["created_utc"]
        post_utc_date_str = current_post["utc_datetime_str"]
        posts_id_list.append({"id": start_post_id, "str_date": post_utc_date_str, "timestamp": post_utc_timestamp})
        start_post_id = None
        for token in post_text.split():
            if "war_in_ukraine_megathread_" in token:
                print(token)
                inner_token_list = token.split("/")
                comment_index = inner_token_list.index("comments")
                start_post_id = inner_token_list[comment_index + 1]
        time.sleep(0.3)
    tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
                      r"Ukraine_War\all_megathreads_post_ids", posts_id_list)


if __name__ == "__main__":
    # a = list()
    # tools.save_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\\"
    #                           r"Ukraine_War\all_megathreads_post_ids_temp", a)
    # crawl_megathreads(start_post_id="uwm88b")
    a = tools.load_pickle(r"C:\Users\irmo\PycharmProjects\Coordination\I_O\Datasets\Ukraine_War\all_megathreads_post_ids")
    print()