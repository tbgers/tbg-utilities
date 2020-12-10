import re
import requests
import pytz
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# get timezones
old_tz = pytz.timezone('Australia/Sydney')
new_tz = pytz.timezone("US/Central")

# First make sure the topic exists (hey, you never know)
response = requests.get('http://tbgforums.com/forums/viewtopic.php?id=4902')
response.raise_for_status()  # make sure the website is okay to parse
tbgSoup = BeautifulSoup(response.text, "lxml")  # website parser

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
for time in range(pages):
    # get the specific page
    response = requests.get(
        f'http://tbgforums.com/forums/viewtopic.php?id=4902&p={(time + 1)}'
    )
    response.raise_for_status()  # make sure it's okay to parse
    tbgSoup = BeautifulSoup(response.text, "lxml")  # website parser

    timestamp_select = tbgSoup.select('h2 > span > a')
    timestamps = ts_regex.findall(str(timestamp_select))
    usernames = [user.text for user in tbgSoup.select('dt strong')]  # find every user
    times.extend(timestamps)
    users.extend(usernames)
    # Uncomment the line below if you want to view the progress.
    print("Finished page %s" % str(time + 1))

# Make sure that each post has a time and a user
assert len(times) == len(users)

# Ignore all posts on the day of the game's creation
del users[:4]
del times[:4]

# Get each time and convert it into CST.
times = [list(time) for time in times]
for time in range(len(times)):
    if times[time][0] == "Today":
        # Today is...today
        today = datetime.now(old_tz).strftime("%Y %b %d").split()
        for j in range(len(today)):
            times[time][j + 2] = today[j]
    elif times[time][0] == "Yesterday":
        # Yesterday is one day ago.
        time_diff = datetime.now(old_tz) - timedelta(1)
        yesterday = time_diff.strftime("%Y %b %d").split()
        for j in range(len(yesterday)):
            times[time][j + 2] = yesterday[j]
    times[time] = times[time][2:]
    dt_obj = datetime.strptime(' '.join(times[time]), '%Y %b %d %H %M %S')
    aedt_to_cst = dt_obj - timedelta(hours=17)
    times[time] = aedt_to_cst

points = []
winners = []
old = datetime(2018, 6, 1, 4, 0, 24).date()
for time in range(len(times)):
    if times[time].date() != old:
        points.append(0)
        if times[time].date().year != old.year:
            if times[time].date().year % 10 == 0:
                points[-1] += 2000
            else:
                points[-1] += 200
        if times[time].date().day == 1:
            points[-1] += 20
        if times[time].date().weekday() == 6:
            points[-1] += 5
        points[-1] += 1
        winners.append(users[time])
        old = times[time].date()

assert len(points) == len(winners)

# Remove duplicate users
data = dict.fromkeys(winners, 0)

for time in range(len(points)):
    data[winners[time]] += points[time]

leaderboard = []
# Put the number of points for each person in a readable format.
for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
    leaderboard.append(f"{k} - " + "{:,}".format(int(v)))

print()
print("\n".join(leaderboard))
