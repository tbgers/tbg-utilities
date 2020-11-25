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

# Make sure that each post has a time and a user
assert len(times) == len(users)

# Get each time and convert it into CST.
times = [list(i) for i in times]
for i in range(len(times)):
    if times[i][0] == "Today":
        # Today is...today
        today = datetime.now(old_tz).strftime("%Y %b %d").split()
        for j in range(len(today)):
            times[i][j + 2] = today[j]
    elif times[i][0] == "Yesterday":
        # Yesterday is one day ago.
        time_diff = datetime.now(old_tz) - timedelta(1)
        yesterday = time_diff.strftime("%Y %b %d").split()
        for j in range(len(yesterday)):
            times[i][j + 2] = yesterday[j]
    times[i] = times[i][2:]
    dt_obj = datetime.strptime(' '.join(times[i]), '%Y %b %d %H %M %S')
    aedt_to_cst = dt_obj - timedelta(hours=17)
    times[i] = aedt_to_cst

# Ignore all posts on the day of the game's creation
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
# Remove duplicate users
data = list(dict.fromkeys(winners))

for i in range(len(points)):
    data[winners[i]] += points[i]

leaderboard = []
# Put the number of points for each person in a readable format.
for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
    leaderboard.append("%s - %s" % (k, "{:,}".format(int(v))))

print()
print("\n".join(leaderboard))
