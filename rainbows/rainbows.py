# import modules
import pygame  # to make a window to display the rainbows
import randomcolor   # to make random colors
from pyperclip import copy  # to copy information to the clipboard
from random import randint  # to select a random rainbow
from pygame.locals import QUIT  # to handle clicking the 'X' on the window
from collections import Counter  # for use in the leaderboard script

# Modules for scraping the rainbow colors
import json
import os
from scrapy.crawler import CrawlerProcess
from rainbows.spiders.rainbow_spider import RainbowSpider

if "rainbows.json" not in os.listdir(os.getcwd()):
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'rainbows.json',
        "ITEM_PIPELINES": {
            "rainbows.pipelines.RainbowsPipeline": 300
        }
    })

    process.crawl(RainbowSpider)
    process.start()

# An entry in rainbows.json is created in the following format:
# {"author": [user], "color": [hex code], "post_id": [post id]}
# Only those that have a purple color (every 6th item) is counted as the finisher.
# If any of the fields are yet to be filled, add "-------" without the quotes.

with open("rainbows.json", "r") as rainbows_file:
    rainbows = json.load(rainbows_file)

while len(rainbows) % 6 != 0:
    rainbows.append({"author": "-------", "color": "-------", "post_id": "-------"})

# Variables
red, orange, yellow, green, blue, purple = (rainbows[i::6] for i in range(6))


def get_rainbow(i):
    # Returns a rainbow tuple from the six lists.
    # Array starts at 1 like a boss
    return (red[i - 1], orange[i - 1], yellow[i - 1], green[i - 1], blue[i - 1], purple[i - 1])


def generate_leaderboard():
    # Finds every use that finished a rainbow, sorts them by number of
    # occurrences, and generates a leaderboard with 1st, 2nd, and 3rd place
    # properly colored with BBCode.
    u = [i["author"] for i in rainbows[5::6] if i["author"] != "-------"]
    data = dict(Counter(u))
    post = []
    for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
        post.append("{} - {}".format(k, "{:,}".format(int(v))))
    post[0] = "[color=#d6a523]" + post[0] + "[/color]"  # Gold
    post[1] = "[color=#a19e9e]" + post[1] + "[/color]"  # Silver
    post[2] = "[color=#cd7f32]" + post[2] + "[/color]"  # Bronze
    copy('\n'.join(post))  # Copy to clipboard
    # Print into console that the operation was successful.
    print("Leaderboard copied to clipboard.")


# Initialize Pygame
pygame.init()

# Set screen
screen = pygame.display.set_mode((960, 720))
pygame.display.set_caption("TBG Rainbows")

# Set fonts
finisher_font = pygame.font.SysFont("consolas", 30)
color_font = pygame.font.SysFont("consolas", 60)
info_font = pygame.font.SysFont("consolas", 15)


def draw(r, draw_info, draw_hex):
    # Get the right rainbow
    index = r
    r = get_rainbow(r)

    for i in range(6):
        # The rectangles display the color themselves.
        # The texts display the hex codes of the colors.
        hex_ = (r[i]["color"].lstrip("#") if r[i]["color"] != "-------" else "ffffff")
        color = tuple(int(hex_[rgb:rgb + 2], 16) for rgb in (0, 2, 4))
        comp = tuple([255 - c for c in color])

        # Draw and color the rectangle
        rect = pygame.Rect(160 * i, 0, 160, 720)
        pygame.draw.rect(screen, color, rect, 0)

        if draw_hex:
            # Display hex codes
            text = color_font.render(r[i]["color"], 1, comp)
            rotated = pygame.transform.rotate(text, 90)
            screen.blit(rotated, (50 + (160 * i), 240))

    if draw_info:
        # Render finisher text
        # Finisher text displays the rainbow number and who finished the
        # rainbow.
        rainbow_number = finisher_font.render(f"Rainbow #{str(index)}", 1, (0, 0, 0))
        if r[-1]["author"] != "-------":
            finisher = finisher_font.render(f"Finished by {r[-1]['author']}", 1, (0, 0, 0))
        else:
            finisher = finisher_font.render("Unfinished", 1, (0, 0, 0))

        # Display finisher text
        screen.blit(rainbow_number, (10, 10))
        screen.blit(finisher, (10, 40))

        # Render info text
        lrarrows = info_font.render("Use the ↔ keys to go up/down a rainbow.", 1, (0, 0, 0))
        udarrows = info_font.render("Use the ↕ keys to go up/down 10 rainbows.", 1, (0, 0, 0))
        space = info_font.render("Use the spacebar to go to a random rainbow.", 1, (0, 0, 0))
        press_t = info_font.render("Press T to toggle info text.", 1, (0, 0, 0))
        press_h = info_font.render("Press H to toggle hex codes.", 1, (0, 0, 0))
        press_l = info_font.render("Press L to copy leaderboard to clipboard.", 1, (0, 0, 0))
        make_colors = info_font.render("Press ROYGBP to copy random hex code for red, orange, etc.", 1, (0, 0, 0))

        # Display info text
        screen.blit(lrarrows, (10, 580))
        screen.blit(udarrows, (10, 600))
        screen.blit(space, (10, 620))
        screen.blit(press_t, (10, 640))
        screen.blit(press_h, (10, 660))
        screen.blit(press_l, (10, 680))
        screen.blit(make_colors, (10, 700))


# Draw first rainbow
rainbow = 1
dt = True
dh = True
draw(rainbow, dt, dh)

# Random color generator
randcolor = randomcolor.RandomColor()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            # Quit program
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Go left a rainbow
                rainbow -= 1
                if rainbow < 1:
                    rainbow = len(red)
            if event.key == pygame.K_RIGHT:
                # Go right a rainbow
                rainbow += 1
                if rainbow > len(red):
                    rainbow = 1
            if event.key == pygame.K_UP:
                # Go right ten rainbows
                for i in range(10):
                    rainbow += 1
                    if rainbow > len(red):
                        rainbow = 1
            if event.key == pygame.K_DOWN:
                # Go left ten rainbows
                for i in range(10):
                    rainbow -= 1
                    if rainbow < 1:
                        rainbow = len(red)
            if event.key == pygame.K_SPACE:
                # Go to a random rainbow
                rainbow = randint(1, len(red))
            if event.key == pygame.K_l:
                # Copy leaderboard data
                generate_leaderboard()
            if event.key == pygame.K_t:
                # Toggle info text
                dt = not dt
            if event.key == pygame.K_h:
                # Toggle hex codes
                dh = not dh
            if event.key == pygame.K_r:  # Generate random shade of red
                hex_code = randcolor.generate(hue="red")[0]
                copy(hex_code)
                print("Red hex code copied to clipboard:")
                print(hex_code)
            if event.key == pygame.K_o:  # Generate random shade of orange
                hex_code = randcolor.generate(hue="orange")[0]
                copy(hex_code)
                print("Orange hex code copied to clipboard:")
                print(hex_code)
            if event.key == pygame.K_y:  # Generate random shade of yellow
                hex_code = randcolor.generate(hue="yellow")[0]
                copy(hex_code)
                print("Yellow hex code copied to clipboard:")
                print(hex_code)
            if event.key == pygame.K_g:  # Generate random shade of green
                hex_code = randcolor.generate(hue="green")[0]
                copy(hex_code)
                print("Green hex code copied to clipboard:")
                print(hex_code)
            if event.key == pygame.K_b:  # Generate random shade of blue
                hex_code = randcolor.generate(hue="blue")[0]
                copy(hex_code)
                print("Blue hex code copied to clipboard:")
                print(hex_code)
            if event.key == pygame.K_p:  # Generate random shade of purple
                hex_code = randcolor.generate(hue="purple")[0]
                copy(hex_code)
                print("Purple hex code copied to clipboard:")
                print(hex_code)
            draw(rainbow, dt, dh)  # Draw rainbow
    pygame.display.update()  # Update screen
