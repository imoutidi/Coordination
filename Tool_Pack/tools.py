import pickle
import time
import datetime
from datetime import date, timedelta

def datetify(date_str):
    if "-" in date_str:
        split_date = date_str.split("-")
        if split_date[0] == "nan":
            result = "nan"
        else:
            result = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    elif "/" in date_str:
        split_date = date_str.split("/")
        if split_date[0] == "nan":
            result = "nan"
        else:
            result = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    else:
        print("Other delimiter in date")
        print(date_str)
        result = "nan"

    return result


def iso_year_start(iso_year):
    # The Gregorian calendar date of the first day of the given ISO year
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    # The Gregorian calendar date for the given ISO year, week and day
    year_start = iso_year_start(iso_year)
    return year_start + timedelta(days=iso_day-1, weeks=iso_week-1)


# Converts a string date time (2020-12-28 01:58:26) into an int timestamp (1609120706)
def str_datetime_to_timestamp(date_str):
    # convert date time string into an object
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(date_obj.timetuple()))
    return timestamp


def timestamp_to_datetime_obj(timestamp):
    # Convert the timestamp to a datetime object in the local timezone
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    return datetime_obj


def save_pickle(path, data_structure):
    save_ds = open(path, "wb")
    pickle.dump(data_structure, save_ds)
    save_ds.close()


def load_pickle(path):
n    load_ds = open(path, "rb")
    data_structure = pickle.load(load_ds)
    load_ds.close()
    return data_structure


if __name__ == "__main__":
    for i in range(1, 51):
        c_date = iso_to_gregorian(2016, i, 1)
        print(str(c_date.year) + " " + str(c_date.month) + " " + str(c_date.day))
