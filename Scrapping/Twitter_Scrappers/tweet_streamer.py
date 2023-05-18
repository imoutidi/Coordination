import json
import tweepy
from datetime import datetime, timezone
import time
import requests
import os
from Tool_Pack import tools

bearer_t = r"AAAAAAAAAAAAAAAAAAAAANyPlgEAAAAAmVIpLSdEJ7y%2BEAgVSQPhUWZGCMg%3DSxrSVwKKjFc2ODviHRybJBzHn" \
           r"VMlcN2JZPPIkB5OLuYFPqE5Sy"
out_path = "/home/iraklis/PycharmProjects/Crypto_Monitor/I_O/Stream_Batches/"


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_t}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_stream(c_date, c_time):
    print(c_date + "_" + c_time)
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at,entities,geo,lang,attachments,author_id"
        , auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))

    with open("/home/iraklis/PycharmProjects/Crypto_Monitor/I_O/Stream_Batches/"
              + c_date + "/" + c_time + ".json", "a") as j_file:
        for idx, response_line in enumerate(response.iter_lines()):
            if response_line:
                json_response = json.loads(response_line)
                j_file.write(json.dumps(json_response) + "\n")
                # print(json.dumps(json_response, indent=4, sort_keys=True))
            if idx > 185:
                break


# Manage stream rules
class MyStream(tweepy.StreamingClient):

    def on_connect(self):
        print("Connected")


def add_rules():
    general_search_terms = ["crypto", "cryptocurrency", "bitcoin", "ethereum", "defi", "decentralized finance",
                            "decentralize", "decentralized apps", "crypto currency", "#crypto", "#defi",
                            "#cryptocurrency", "blockchain", "#bitcoin", "#blockchain"]
    stream = MyStream(bearer_token=bearer_t, wait_on_rate_limit=True)
    for term in general_search_terms:
        stream.add_rules(tweepy.StreamRule(term))


def delete_all_rules():
    stream = MyStream(bearer_token=bearer_t, wait_on_rate_limit=True)
    rule_ids = [x.id for x in stream.get_rules()[0]]
    stream.delete_rules(rule_ids)
    print(stream.get_rules())

class Streamer():
    def __init__(self):
        self.hashtags = ["#εκλογες_2023", "#εκλογες2023", "#ΣΥΡΙΖΑ", "#ΣΥΡΙΖΑ_ΠΣ ", "#Εκλογες_21__Μαιου",  "#Τσιπρας",
                         "#Εκλογες_21__Μαιου", "#ΠΑΣΟΚ", "#ΝΔ", "#ΚΚΕ", "#ΜέΡΑ25", "#MeRA25", "#Βελοπουλος"]
        self.users = ["@kmitsotakis", "@atsipras", "@syriza_gr", "@neademokratia", "@gt_kke", "@mera25_gr",
                      "@varoufakis_gr", "@velopky"]
        self.keywords = ["ΝΕΑ ΔΗΜΟΚΡΑΤΙΑ", "νέα δημοκρατία", "ΚΚΕ", "ΣΥΡΙΖΑ", "σύριζα", "ΠΑΣΟΚ", "πασόκ", "Μητσοτάκης",
                         "Τσίπρας", "Κουτσούμπας", "Βαρουφάκης", "ΜΕΡΑ25"]


if __name__ == "__main__":
    while True:
        if datetime.now(timezone.utc).second == 4:
            only_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            only_time = datetime.now(timezone.utc).strftime("%H:%M")
            if not os.path.exists(out_path + only_date):
                os.makedirs(out_path + only_date)
            get_stream(only_date, only_time)
            # Sleep call in case get_steam() return too fast
            sleep_time = 56 - datetime.now(timezone.utc).second
            print(sleep_time)
            if sleep_time > 0:
                time.sleep(sleep_time)


