# first.py http://tbgforums.com/forums/viewtopic.php?id=4902
# This script will output a copy-and-paste leaderboard for the topic "First"
# The score is based on the first person to post on a specific day. Users get
# more points if they are the first to post in a week, month, year, etc.

# Following is the point chart for being first to post in a...
# day = 1 point
# week = 5 points
# month = 20 points
# year = 200 points
# decade = 2000 points
# The point chart stops here, but assuming the same pattern for years...
# century = 20000 points
# millennium = 200000 points
# megaannum = 2000000 points
# gigaannum = 20000000 points
# ...and so on. But realistically we will never reach this point, so it's not
# going to be coded beyond "decade"

# Things to consider:
# The web is scraped in the AEDT time zone
# Whether or not daylight saving time is in effect (idk about Arizona, Hawaii,
# or other countries)
# Game is played in central time, so the program will detect the timezone of the
# local system and make differences accordingly

# import modules
import re
import requests
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# get timezones
old_tz = pytz.timezone('Australia/Sydney')
new_tz = pytz.timezone("US/Central")

# First make sure the topic exists (hey, you never know)
r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=4902')
r.raise_for_status()  # make sure the website is okay to parse
tbgSoup = BeautifulSoup(r.text, "lxml")  # website parser

# Find out how many pages we have to go through.
users = []  # list of people that posted
times = []  # list of each post's timestamp
pages = int(tbgSoup.select('.pagelink')[
            0].text.split(' ')[-2])  # number of pages

ts_regex = re.compile(r'''
                          ((Today|Yesterday)|(\d{4})-([A-Z][a-z]{2})-(\d{2}))
                          \s+
                          (\d{1,2}):(\d{2}):(\d{2})
                          ''', re.VERBOSE)
# Go through each page and get all the users that posted on that page.
for i in range(pages):
    r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=4902&p=%s' %
                     str(i + 1))  # get the specific page
    r.raise_for_status()  # make sure it's okay to parse
    tbgSoup = BeautifulSoup(r.text, "lxml")  # website parser

    timestamp_select = tbgSoup.select('h2 > span > a')
    timestamps = ts_regex.findall(str(timestamp_select))
    usernames = [i.text for i in tbgSoup.select('dt strong')]  # find every user
    times.extend(timestamps)
    users.extend(usernames)
    # Uncomment the line below if you want to view the progress.
    print("Finished page %s" % str(i + 1))

assert len(times) == len(users)

times = [list(i) for i in times]
for i in range(len(times)):
    if times[i][0] == "Today":
        today = datetime.now(old_tz).strftime("%Y %b %d").split()
        for j in range(len(today)):
            times[i][j + 2] = today[j]
    elif times[i][0] == "Yesterday":
        time_diff = datetime.now(old_tz) - timedelta(1)
        yesterday = time_diff.strftime("%Y %b %d").split()
        for j in range(len(yesterday)):
            times[i][j + 2] = yesterday[j]
    times[i] = times[i][2:]
    dt_obj = datetime.strptime(' '.join(times[i]), '%Y %b %d %H %M %S')
    aedt_to_cst = dt_obj - timedelta(hours=17)
    times[i] = aedt_to_cst

del users[:4]
del times[:4]

points = []
winners = []
old = datetime(2018, 6, 1, 4, 0, 24).date()
for i in range(len(times)):
    if times[i].date() != old:
        points.append(0)
        if times[i].date().year % 10 == 0:
            points[-1] += 2000
        if times[i].date().year != old.year:
            points[-1] += 200
        if times[i].date().day == 1:
            points[-1] += 20
        if times[i].date().weekday() == 6:
            points[-1] += 5
        points[-1] += 1
        winners.append(users[i])
        old = times[i].date()

assert len(points) == len(winners)

zeroes = [0 for i in points]
# This conveniently removes duplicate users, so yay!
data = dict(zip(winners, zeroes))

for i in range(len(points)):
    data[winners[i]] += points[i]

leaderboard = []
# Put the number of points for each person in a readable format.
for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
    leaderboard.append("%s - %s" % (k, "{:,}".format(int(v))))

print(leaderboard)