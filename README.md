# tbg-utilities
Some utilities for the Text Based Games Forums (http://tbgforums.com/forums)

They are mostly for updating leaderboards, maybe posting content every now and then, etc. If you would like to contribute by making a utility of your own, feel free to do so. Any language is acceptable, but Python is preferred. You can also choose to fix bugs or make utilities more efficient.

## Rainbows (script: `rainbows/rainbows.py`)
Display all the rainbows from Rainbows (https://tbgforums.com/forums/viewtopic.php?id=2956).

The rainbows list is automatically scraped from the topic using Scrapy. When the script is run for the first time, it will get posts from the topic and update the rainbows. The rainbow data is stored in `rainbows.json`. For now, to manually update the list, simply delete the `rainbows.json` file.

## First (script: `scores/first.py`)
Print the leaderboard for First (http://tbgforums.com/forums/viewtopic.php?id=4902)

The score is based on the first person to post on a specific day. Users get more points if they are the first to post in a week, month, year, etc.

The following is the point chart for being first to post in a...
day = 1 point
week = 5 points
month = 20 points
year = 200 points
decade = 2000 points
century = 20000 points
millennium = 200000 points
megaannum = 2000000 points
gigaannum = 20000000 points
...and so on. But realistically we will never reach past "decade," so the script only goes up to a decade.

Things to consider:
- The web is scraped in the AEDT time zone
- Whether or not daylight saving time is in effect
- Game is played in central time, so the program will detect the timezone of the local system and make differences accordingly

## The sky is the limit. (script: `scores/tsitl.py`)
Print the leaderboard for The sky is the limit. (https://tbgforums.com/forums/viewtopic.php?id=170)

One of the simpler scripts, because it simply counts the number of times someone posts on the topic. It also auto-formats the leaderboard with 1st, 2nd, and 3rd place having gold, silver, and bronze coloring, respectively.
---

## Upcoming topics

Hold the last post for as long as possible (http://tbgforums.com/forums/viewtopic.php?id=5145)

Thread Necromancy Game (http://tbgforums.com/forums/viewtopic.php?id=2111)

Add / Remove / Change A Letter (http://tbgforums.com/forums/viewtopic.php?id=2670)
