# import modules
import pygame
import pyperclip
import random
import urllib.request
from pygame.locals import QUIT
from collections import Counter

# Get all rainbows from rbs.txt, which (for now) is updated manually.

# An entry in rbs.txt is created in the following format:
# RED HEX CODE
# ORANGE HEX CODE
# YELLOW HEX CODE
# GREEN HEX CODE
# BLUE HEX CODE
# PURPLE HEX CODE
# USER WHO FINISHED THE RAINBOW
# If any of the fields are yet to be filled, add "--TBD--" without the quotes.

with open("rbs.txt") as f:
    rainbows = f.read().splitlines()

# Variables
r, o, y, g, b, p, user = (rainbows[i::7] for i in range(7))


def get_rainbow(i):
    # Gets the corresponding rainbow
    return (r[i - 1], o[i - 1], y[i - 1], g[i - 1], b[i - 1], p[i - 1],
            user[i - 1])


def generate_leaderboard():
    # Script borrowed and tweaked from TSITL.py
    u = [i for i in user if i != "--TBD--"]
    data = dict(Counter(u))
    post = []
    for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
        post.append("{} - {}".format(k, "{:,}".format(int(v))))
    post[0] = "[color=#d6a523]" + post[0] + "[/color]"  # Gold
    post[1] = "[color=#a19e9e]" + post[1] + "[/color]"  # Silver
    post[2] = "[color=#cd7f32]" + post[2] + "[/color]"  # Bronze
    pyperclip.copy('\n'.join(post))
    print("Leaderboard copied to clipboard.")


# Initialize Pygame
pygame.init()

# Set screen
screen = pygame.display.set_mode((960, 720))
pygame.display.set_caption("TBG Rainbows")

# Set fonts
finisher_font = pygame.font.SysFont("consolas", 30)
color_font = pygame.font.SysFont("consolas", 60)


def draw(r, draw_text):
    index = r
    r = get_rainbow(r)

    for i in range(6):
        # The rectangles display the color themselves.
        # The texts display the hex codes of the colors.
        hex = (r[i].lstrip("#") if r[i] != "--TBD--" else "000000")
        color = tuple(int(hex[rgb:rgb + 2], 16) for rgb in (0, 2, 4))
        comp = tuple([255 - c for c in color])

        rect = pygame.Rect(160 * i, 0, 160, 720)  # Draw the rectangles
        pygame.draw.rect(screen, color, rect, 0)
        if draw_text:
            text = color_font.render(r[i], 1, comp)  # Draw the texts
            rotated = pygame.transform.rotate(text, 90)
            screen.blit(rotated, (50 + (160 * i), 240))

    # Display who finished the rainbow
    if draw_text:
        if r[-1] != "--TBD--":
            finisher = finisher_font.render("Rainbow #" + str(index) +
                                            ": Finished by " + r[-1], 1,
                                            (0, 0, 0))
        else:
            finisher = finisher_font.render("Rainbow #" + str(index) +
                                            ": Unfinished", 1, (0, 0, 0))
        screen.blit(finisher, (10, 10))


# Draw first rainbow
rainbow = 1
dt = True
draw(rainbow, dt)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rainbow -= 1
                if rainbow < 1:
                    rainbow = len(r)
            if event.key == pygame.K_RIGHT:
                rainbow += 1
                if rainbow > len(r):
                    rainbow = 1
            if event.key == pygame.K_SPACE:
                rainbow = random.randint(1, len(r))
            if event.key == pygame.K_l:
                generate_leaderboard()
            if event.key == pygame.K_t:
                dt = not dt
            draw(rainbow, dt)
    pygame.display.update()
