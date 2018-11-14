import pygame
import random
from pygame.locals import QUIT

with open('rbs.txt') as f:
    rainbows = f.read().splitlines()

r, o, y, g, b, p, user = (rainbows[i::7] for i in range(7))


def get_rainbow(i):
    return (r[i - 1], o[i - 1], y[i - 1], g[i - 1], b[i - 1], p[i - 1],
            user[i - 1])


pygame.init()

screen = pygame.display.set_mode((960, 720))
pygame.display.set_caption("TBG Rainbows")

finisher_font = pygame.font.SysFont("consolas", 30)

rainbow = 1


def draw(r):
    r = get_rainbow(r)
    rects = (pygame.Rect(160 * i, 0, 160, 720) for i in range(6))
    red, orange, yellow, green, blue, purple = rects

    counter = 0
    for i in [red, orange, yellow, green, blue, purple]:
        hex = (r[counter].lstrip("#") if r[counter] != "N/A" else "000000")
        color = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        pygame.draw.rect(screen, color, i, 0)
        counter += 1

    finisher = finisher_font.render("Finished by "+r[-1], 1, (0, 0, 0))
    screen.blit(finisher, (10, 10))


draw(rainbow)

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
            draw(rainbow)
    pygame.display.update()