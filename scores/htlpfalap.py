import calendar
from datetime import datetime, timedelta
import re

import pytz
import requests
from bs4 import BeautifulSoup

# Get AEDT timezone
aedt = pytz.timezone('Australia/Sydney')

# Get a response from the topic
r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=5145')
r.raise_for_status()  # make sure the website is okay to parse
tbgSoup = BeautifulSoup(r.text, "lxml")  # website parser

# Find out how many pages we have to go through.
users = []  # list of people that posted
times = []  # list of each post's timestamp
pages = int(tbgSoup.select(".pagelink")[
            0].text.split(" ")[-2])  # number of pages

ts_regex = re.compile(r'''
                          ((Today|Yesterday)|(\d{4})-([A-Z][a-z]{2})-(\d{2}))
                          \s+
                          (\d{1,2}):(\d{2}):(\d{2})
                          ''', re.VERBOSE)

# Go through each page and get all the users that posted on that page.
for time in range(pages):
    # get the specific page
    r = requests.get(f"http://tbgforums.com/forums/viewtopic.php?id=5145&p={time + 1}")
    r.raise_for_status()  # make sure it's okay to parse
    tbgSoup = BeautifulSoup(r.text, "lxml")  # website parser

    timestamp_select = tbgSoup.select("h2 > span > a")
    timestamps = ts_regex.findall(str(timestamp_select))

    usernames = [i.text for i in tbgSoup.select("dt strong")]  # find every user

    times.extend(timestamps)
    users.extend(usernames)

    # Uncomment the line below if you want to view the progress.
    print(f"Finished page {time + 1} of {pages}")

# Make sure that each post has a time and a user
assert len(times) == len(users)

# Ignore the first post
del users[0]
del times[0]


# Convert every timestamp into a datetime object
def convert_to_datetime(tup):
    if tup[0] == "Today":
        # Today is...today
        today = datetime.now(aedt).strftime("%Y %b %d").split()

        year = int(today[0])
        month = list(calendar.month_abbr).index(today[1])
        day = int(today[2])
    elif tup[0] == "Yesterday":
        # Yesterday is one day ago.
        time_diff = datetime.now(aedt) - timedelta(1)
        yesterday = time_diff.strftime("%Y %b %d").split()

        year = int(yesterday[0])
        month = list(calendar.month_abbr).index(yesterday[1])
        day = int(yesterday[2])
    else:
        # Any other day is represented by an actual timestamp
        year = int(tup[2])
        month = list(calendar.month_abbr).index(tup[3])
        day = int(tup[4])

    return datetime(
        year=year,
        month=month,
        day=day,
        hour=int(tup[5]),
        minute=int(tup[6]),
        second=int(tup[7])
    )


times = [convert_to_datetime(time) for time in times]

scores = []


# Find the time difference between two different times in total seconds
def find_time_diff(initial_time, final_time):
    time_diff = final_time - initial_time

    # Keep track of the seconds
    sec_rounded = time_diff.total_seconds()
    # Smaller minute
    s_min = (sec_rounded // 60) * 60
    # Larger minute
    l_min = s_min + 60
    # Round to the nearest minute
    sec_rounded = l_min if sec_rounded - s_min > l_min - sec_rounded else s_min

    return sec_rounded


for time in range(len(times) - 1):
    scores.append(timedelta(seconds=find_time_diff(times[time], times[time + 1])))

assert len(scores) + 1 == len(users)

# Remove duplicate users
data = dict.fromkeys(users, timedelta(seconds=0))

for time in range(len(scores)):
    data[users[time]] += scores[time]


# Convert each timedelta object into a readable format.
def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ("y", 60 * 60 * 24 * 365),
        ("w", 60 * 60 * 24 * 7),
        ("d", 60 * 60 * 24),
        ("h", 60 * 60),
        ("m", 60)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            strings.append(f"{period_value}{period_name}")

    return " ".join(strings)


leaderboard = []
counter = 1
# Put the timedeltas for each person in a readable format.
for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
    leaderboard.append(f"#{counter}: {k} - {td_format(v)}")
    counter += 1

# Add coloring for first, second, and third place
leaderboard[0] = "[color=gold]" + leaderboard[0] + "[/color]"
leaderboard[1] = "[color=silver]" + leaderboard[1] + "[/color]"
leaderboard[2] = "[color=orange]" + leaderboard[2] + "[/color]"

print()
print("\n".join(leaderboard))

now = datetime.now(pytz.timezone('UTC'))
now_in_aedt = now.astimezone(aedt).replace(tzinfo=None)
current_bonus = timedelta(seconds=find_time_diff(times[-1], now_in_aedt))

print()
print(f"Currently, {users[-1]} can earn up to {td_format(current_bonus)}")
