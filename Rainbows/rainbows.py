# import modules
import pygame  # to make a window to display the rainbows
import randomcolor   # to make random colors
from pyperclip import copy  # to copy information to the clipboard
from random import randint  # to select a random rainbow
from pygame.locals import QUIT  # to handle clicking the 'X' on the window
from collections import Counter  # for use in the leaderboard script

# An entry in rbs.txt is created in the following format:
# RED HEX CODE
# ORANGE HEX CODE
# YELLOW HEX CODE
# GREEN HEX CODE
# BLUE HEX CODE
# PURPLE HEX CODE
# USER WHO FINISHED THE RAINBOW
# If any of the fields are yet to be filled, add "-------" without the quotes.

with open("rbs.txt") as f:
    # Get all rainbows from rbs.txt, which (for now) is updated manually.
    rainbows = f.read().splitlines()

# Variables
r, o, y, g, b, p, user = (rainbows[i::7] for i in range(7))


def get_rainbow(i):
    # Returns a rainbow tuple from the seven lists.
    # Array starts at 1 like a boss
    return (r[i - 1].lower(), o[i - 1].lower(), y[i - 1].lower(),
            g[i - 1].lower(), b[i - 1].lower(), p[i - 1].lower(),
            user[i - 1])


def generate_leaderboard():
    # Script borrowed and tweaked from TSITL.py
    # Finds every use that finished a rainbow, sorts them by number of
    # occurrences, and generates a leaderboard with 1st, 2nd, and 3rd place
    # properly colored with BBCode.
    u = [i for i in user if i != "-------"]
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
        hex = (r[i].lstrip("#") if r[i] != "-------" else "ffffff")
        color = tuple(int(hex[rgb:rgb + 2], 16) for rgb in (0, 2, 4))
        comp = tuple([255 - c for c in color])

        # Draw and color the rectangle
        rect = pygame.Rect(160 * i, 0, 160, 720)
        pygame.draw.rect(screen, color, rect, 0)

        if draw_hex:
            # Display hex codes
            text = color_font.render(r[i], 1, comp)
            rotated = pygame.transform.rotate(text, 90)
            screen.blit(rotated, (50 + (160 * i), 240))

    if draw_info:
        # Render finisher text
        # Finisher text displays the rainbow number and who finished the
        # rainbow.
        if r[-1] != "-------":
            finisher = finisher_font.render("Rainbow #" + str(index) +
                                            ": Finished by " + r[-1], 1,
                                            (0, 0, 0))
        else:
            finisher = finisher_font.render("Rainbow #" + str(index) +
                                            ": Unfinished", 1, (0, 0, 0))
        # Display finisher text
        screen.blit(finisher, (10, 10))

        # Render info text
        lrarrows = info_font.render("Use the ↔ keys to go up/down a rainbow.",
                                    1, (0, 0, 0))
        udarrows = info_font.render("Use the ↕ keys to go up/down 10 rainbows.",
                                    1, (0, 0, 0))
        space = info_font.render("Use the spacebar to go to a random rainbow.",
                                 1, (0, 0, 0))
        press_t = info_font.render("Press T to toggle info text.", 1, (0, 0, 0))
        press_h = info_font.render("Press H to toggle hex codes.", 1, (0, 0, 0))
        press_l = info_font.render("Press L to copy leaderboard to clipboard.",
                                   1, (0, 0, 0))
        colors = "Press ROYGBVP to copy random hex code for red, orange, etc."
        make_colors = info_font.render(colors, 1, (0, 0, 0))

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
                    rainbow = len(r)
            if event.key == pygame.K_RIGHT:
                # Go right a rainbow
                rainbow += 1
                if rainbow > len(r):
                    rainbow = 1
            if event.key == pygame.K_UP:
                # Go right ten rainbows
                for i in range(10):
                    rainbow += 1
                    if rainbow > len(r):
                        rainbow = 1
            if event.key == pygame.K_DOWN:
                # Go left ten rainbows
                for i in range(10):
                    rainbow -= 1
                    if rainbow < 1:
                        rainbow = len(r)
            if event.key == pygame.K_SPACE:
                # Go to a random rainbow
                rainbow = randint(1, len(r))
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
