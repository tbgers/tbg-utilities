import requests
from bs4 import BeautifulSoup
from collections import Counter

r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=170')
r.raise_for_status()
tbgSoup = BeautifulSoup(r.text, "lxml")

posters = []
pages = int(tbgSoup.select('.pagelink')[0].text.split(' ')[-2])

for i in range(pages):
    r = requests.get('http://tbgforums.com/forums/viewtopic.php?id=170&p=%s' % str(i+1))
    r.raise_for_status()
    tbgSoup = BeautifulSoup(r.text, "lxml")
    p = tbgSoup.select('dt strong')
    for j in p:
        posters.append(j.text)
    print("Finished page %s" % str(i+1))

data = dict(Counter(posters))
print()
post = []

for k,v in sorted(data.items(), key=lambda p:p[1], reverse=True):
    if int(v) > 1:
        post.append("%s: %s points." % (k,"{:,}".format(int(v))))
    else:
        post.append("%s: 1 point." % k)
        
post[0] = "[color=#d6a523][1] " + post[0] + "[/color]"
post[1] = "[color=#a19e9e][2] " + post[1] + "[/color]"
post[2] = "[color=#cd7f32][3] " + post[2] + "[/color]"

for i in range(3, len(data)):
    post[i] = ("[%s] " % str(i+1)) + post[i]

for i in post:
    print(i)
