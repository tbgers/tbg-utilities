# import the necessary modules
import requests
from bs4 import BeautifulSoup
from collections import Counter

# First make sure the topic exists (hey, you never know)
r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=170')
r.raise_for_status()  # make sure the website is okay to parse
tbgSoup = BeautifulSoup(r.text, "lxml")  # website parser

# Find out how many pages we have to go through.
posters = []  # list of people that posted
pages = int(tbgSoup.select('.pagelink')[
            0].text.split(' ')[-2])  # number of pages

# Go through each page and get all the users that posted on that page.
for i in range(pages):
    r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=170&p=%s' %
                     str(i + 1))  # get the specific page
    r.raise_for_status()  # make sure it's okay to parse
    tbgSoup = BeautifulSoup(r.text, "lxml")  # website parser
    p = tbgSoup.select('dt strong')  # find every username
    for j in p:  # for every username...
        posters.append(j.text)  # ...add it to the list of posters.
    # Uncomment the line below if you want to view the progress.
    # print("Finished page %s" % str(i+1))

# Find out how many times every user appears in posters.
# Make a counter for every occurrence of every person
data = dict(Counter(posters))
print()
post = []

# Put the number of points for each person in a readable format.
for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
    if int(v) > 1:
        post.append("%s: %s points." % (k, "{:,}".format(int(v))))
    else:
        post.append("%s: 1 point." % k)

# Add gold, silver, and bronze colors for first, second, and third place,
# respectively.
post[0] = "[color=#d6a523][1] " + post[0] + "[/color]"  # Gold
post[1] = "[color=#a19e9e][2] " + post[1] + "[/color]"  # Silver
post[2] = "[color=#cd7f32][3] " + post[2] + "[/color]"  # Bronze

# Add numbers to indicate position for 4th place and below.
for i in range(3, len(data)):
    post[i] = ("[%s] " % str(i + 1)) + post[i]

# Print the pretty, formatted leaderboard. It's now ready to Ctrl+C Ctrl-V!
for i in post:
    print(i)
