import pygame
import time
import random
from pygame.locals import *
from module.Robot import *
# this function will show message on the displayed window
def message_to_screen(message, color, x, y, surface):
    """ Create a text and display it at certain point

    Parameters
    ----------
    message: str
        the text you want to show
    color: Color
        the color of the text
    x: int
        the x coordinate of the position of the text
    y: int
        the y coordinate of the position of the text
    surface:
        the surface that the text will be put on

    Returns
    -------
    No returns

    """
    # initialize the font and its size
    font = pygame.font.SysFont(None, 25)
    # create the text by certain standard
    screen_text = font.render(message, True, color)
    # stick the screen_text to the surface
    surface.blit(screen_text, (x, y))




def level_chosen(surface):
    """ this method will let the player choose the level of the game

        the different level button will be triggered and the game_loop
        will be called with differetn parameters in it represents the
        diffrent monster velocity

    Parameters
    ----------
    surface:
        the displayed window

    Returns
    -------
    No returns

    """
    # initialize choosing to control the choose level stage loop
    choosing = True
    # while the player hasn't make a choice
    while choosing:
        # if the player hit quit, then quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # make the background color black
        surface.fill((0,0,0))

        # stick the difficulty button
        button(surface, 'easy', 20, 200, 100, 30, (0,0,200),(0,0,255),(255,255,255), action = 'easy')

        button(surface, 'medium', 200, 200, 100, 30, (200,200,0),(255,255,0),(255,255,255), action = 'medium')

        button(surface, 'difficult', 380,200, 100, 30, (200,0,0),(255,0,0),(255,255,255), action = 'difficult')

        # update the screen
        pygame.display.update()


def button(surface, msg, x, y, width, height, inactive_color, active_color, msg_color, action = None):
    """ Create a button for users to make choice

        If the mouse is at the expected button area, draw the rectangle with
        active_color at the expected area.
        If the mouse is not at the expected button area, draw the rectangle
        with inactivve_color at the expected area.

    Parameters
    ----------
    surface:
        the surface that the message will lay on
    msg:  str
        the message that you want to show on the button
    x:   int
        the x-coordinate of the button's top left  corner
    y:   int
        the y-coordinate of the button's top left corner
    width:  int
        the width of the button
    height: int
        the height of the button
    active_color:  color
        the color of the button when your mouse position is on the button
    inactive_color: color
        the color of the button when your mouse position is not on the button
    msg_color:  color
        the color of the message that will show on the button
    action:  str
        the action the button will do

    """
    # create mouse and click object to detect mouse behavior
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # if mouse is put on the button, highlight the button
    # if the mouse clicks the button, execute the if cell

    # if mouse is put in the button area
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        # draw a rectangle with active_color
        pygame.draw.rect(surface, active_color, (x,y,width,height))
        # if the mouse clicks 'start' button, call the level_chosen function
        if click[0] == 1 and action == 'start':
            level_chosen(surface)

        # if the mouse clicks 'end' button, quit the game
        if click[0] == 1 and action == 'end':
            pygame.quit()
            exit()

        # if the mouse clicks 'play again' button, call the level_chosen function
        if click[0] == 1 and action == 'play again':
            level_chosen(surface)

        # choose the level
        if click[0] == 1 and action == 'easy':
            game_loop(surface, 500, 500, 10)

        if click[0] == 1 and action == 'medium':
            game_loop(surface, 500, 500, 20)

        if click[0] == 1 and action == 'difficult':
            game_loop(surface, 500, 500, 30)

    # if the mouse is not put on the button area, draw a rectangle with
    # inactive_color at the certain area
    else:
        pygame.draw.rect(surface, inactive_color,(x, y, width, height))

    # stick the text represents the behavior of the button on the button
    message_to_screen(msg, msg_color, x + width/3 , y + height/3, surface)


def game_loop(surface, screen_width, screen_height, input_monster_vel = 5):
    """ contains the main loop of the game

    Parameters
    ----------
    surface:
        the displayed window of the game
    screen_width: int
        the width of the screen
    screen_height: int
        the height of the screen
    input_monster_vel: int (default as 5)
        the velocity of the monster, varies by the difficulty of the game

    Returns
    -------
    Its an operation method, so no returns

    """

    # the music player control
    play_music = True
    # the position and dimention of player
    player_x = 50
    player_y = 50
    player_width = 50
    player_height = 60

    # the position and dimension of monster
    monster_x = 400
    monster_y = 400
    monster_width = 30
    monster_height = 25

    # velocity of the moving character
    player_vel = 20
    monster_vel = input_monster_vel

    # load the image of the figure
    image_player = pygame.image.load('media/grace.png')
    image_monster = pygame.image.load('media/monster.jpg')

    # random chosen position
    rand_x = random.randint(20,screen_width-20)
    rand_y = random.randint(20,screen_height-20)

    # whether the food is eaten by player in that iteration
    is_eaten = False
    # whether the while loop continues
    running = True
    # whether the player is killed by the monster
    is_killed = False
    # whether the certain game continue
    this_game_continue = True

    # the score Grace gained
    score = 0

    # the player in the game
    player = Player(player_width, player_height)
    # the monster in the game
    monster = Monster(monster_width, monster_height)
    # the food in the game
    food =  Food_to_eat()

    # the main loop
    while running or this_game_continue:

        pygame.time.delay(5)

        # play background music
        if play_music:
            pygame.mixer.music.load('media/bgm.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            play_music = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

        if this_game_continue:
            keys = pygame.key.get_pressed()
            surface.fill((0,0,0))

            # let player move and update its position
            player_x, player_y = player.move(surface,player_x,player_y,keys,player_vel,image_player,screen_width,screen_height)

            # let monster move and update its position
            monster_x, monster_y = monster.move(surface,monster_x,monster_y,monster_vel,image_monster,screen_width,screen_height)

            # let food show
            food.show(surface,rand_x,rand_y)

            # detect whether the monster touches the player
            is_killed = monster.kill_or_not(player)

        if is_killed:
            # play again button and end button
            button(surface, 'Play Again', 150, 150, 200,200, (0, 200, 0), (0, 255, 0), (255, 255, 255), 'play again')
            button(surface, 'end', 400, 400 , 80, 30, (200, 0, 0), (255, 0, 0), (255, 255, 255), 'end')
            # this game ends, but the while loop continues
            this_game_continue = False
            pygame.display.update()

        # detect whether the food is eaten, if it is, put a new food position
        if this_game_continue:
            is_eaten = food.eat_or_not(player)
            # if the food is eaten, give the food a new position
            if is_eaten:
                is_eaten = False
                score += 5
                rand_x = random.randint(20,screen_width-20)
                rand_y = random.randint(20,screen_height-20)

        # show the score Grace has on the screen_text
        score_text = 'Score: ' + str(score)
        message_to_screen(score_text, (255,255,255), 0, 480, surface)

        # update the surface
        pygame.display.update()

    # message_to_screen('finished', (255,0,0), screen_width/2, screen_height/2)
    pygame.display.update()

    not_exist = True
    # this is to make sure the game can be quited at any time
    while not_exist:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
