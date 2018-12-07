import pygame
import time
import random
from pygame.locals import *

from module.my_function import *
from module.Robot import *

# initialize the mixer for bgm using
pygame.mixer.pre_init(44100,-16,2,4096)
# initialize pygame
pygame.init()

# set the screen size
screen_width = 500
screen_height = 500
win = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Duolan's Final Project Game")

# set clock for tge game
clock = pygame.time.Clock()

# the introduction control
intro_or_not = False

# initialize the font and its size
font = pygame.font.SysFont(None, 25)

rule_part1 = 'you are Grace, try to move yourself to get the white dot,'
rule_part2 = 'and do not get caught by the monster!'


def game_intro():
    """ the introduction stage of the game

        the game_intro will be triggered, and if the 'start' button is clicked,
        the level_chosen method will be called.

    Parameters
    ----------
    No

    Returns
    -------
    No

    """

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # fill the background with black
        win.fill((0,0,0))

        # stick the rule to the surface
        message_to_screen(rule_part1, (255,255,255), 20,20, win)
        message_to_screen(rule_part2, (255,255,255), 20,40, win)

        # create the start and end button
        button(win, 'start', 100, 200, 150, 40, (0, 200, 0), (0, 255, 0), (200, 200, 200), 'start')

        button(win, 'end', 300, 200, 150, 40, (200, 0, 0), (255, 0, 0), (200, 200, 200), 'end' )

        # update the display window
        pygame.display.update()

        clock.tick(5)


# call the game_intro, this is the call that start the game
game_intro()
