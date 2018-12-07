# this file contains all the class that related to the Robot.

import pygame
import time
import random
from pygame.locals import *

class Bot():

    """
    Class Bot defines a moving bot with rectangle shape, that will move on the screen.

    Args:
        width(int): the width of the bot
        height(int): the height of the bot

    Attributes:
        width(int): the width of the bot
        height(int): the height of the bot
        bot_x: the x coordinate of the position of the bot
        bot_y: the y coordinate of the position of the bot

    class method:
        move():
            move the bot

    """
    def __init__(self,width,height):
        self.width = width
        self.height = height
        # initialize the position of the bot at (0,0)
        self.bot_x = 0
        self.bot_y = 0

    def move(self,surface,x,y,keys,vel,image,screen_width,screen_height):
        """ Move the bot
        Note: the bot can only move inside the surface,
              when it is about to touch the edge, it stops.

        Parameters
        ----------
        surface:
            the surface that the bot stays on
        x:   int
            the x coordinate of bot's current position
        y:   int
            the y coordinate of the bot's current position
        keys:
            the key that player presses in that certain game loop
        vel:    int
            the velocity of the moving bot
        image:
            the image that will 'stick' to the rectangle
        screen_width:  int
            the width of the surface screen
        screen_height: int
            the height of the surface screen

        Returns
        -------
        bot_x: int
            the x coordinate of the current position of the bot
        bot_y: int
            the y coordinate of the current position of the bot

        """
        self.bot_x = x
        self.bot_y = y

        # put the image on the screen
        surface.blit(image,(self.bot_x,self.bot_y))

        # take the keys and decide the moving direction
        # the statement before and decide the potential moving direction,
        # and the statement behind the and checks wheter the position of the bot
        # satisfies the requirment, stays inside the screen.
        if keys[pygame.K_LEFT] and self.bot_x > vel:
            self.bot_x -= vel
        if keys[pygame.K_RIGHT] and self.bot_x < screen_width - self.width - vel:
            self.bot_x += vel
        if keys[pygame.K_UP] and self.bot_y > vel:
            self.bot_y -= vel
        if keys[pygame.K_DOWN] and self.bot_y < screen_height - self.height - vel:
            self.bot_y += vel
        # return the updated position
        return self.bot_x,self.bot_y


class Player(Bot):
    """ Class Player is a subclass that inherits from class Bot.
        They are the same thing, but for clearence, we will use a class.

    Args:
        width(int): the width of the player
        height(int): the height of the player

    Attributes:
        width(int): the width of the player
        height(int): the height of the player
        bot_x: the x coordinate of the position of the player
        bot_y: the y coordinate of the position of the player

    class method:
        move():
            move the player

    """
    def __init__(self,width,height):
        super().__init__(width,height)


class Monster(Bot):
    """
    Class Monster defines a monster that will show up in the game. This class
    inherits from the Bot Class, but the move method is re defined, and there
    are some new methods added in.

    Args:
        width(int): the width of the monster
        height(int): the height of the monster

    Attributes:
        width(int): the width of the monster
        height(int): the height of the monster
        last_move(str): the direction of the last move
        x: the x coordinate of the current location
        y: the y coordinate of the current location

    Methods:
        move():
            move the monster
        kill_or_not():
            decide whether the in-game player is killed by this monster

        """

    def __init__(self,width,height):
        super().__init__(width,height)
        # declare the last_move so it can choose biased  movement or not
        self.last_move = None
        # to prevent the monster and the player have the same start point
        # we put the monster at the right-bottom corner of the screen
        self.x = 400
        self.y = 400

    def move(self,surface,x,y,vel,image,screen_width,screen_height):
        """
        Note: the bot can only move inside the surface,
              when it is about to touch the edge, it stops.

        Parameters
        ----------
        surface:
            the surface that the monster stays on
        x:   int
            the x coordinate of monster's current position
        y:   int
            the y coordinate of the monster's current position
        keys:
            the key that player presses in that certain game loop
        vel:    int
            the velocity of the moving monster
        image:
            the image that will 'stick' to the rectangle
        screen_width:  int
            the width of the surface screen
        screen_height: int
            the height of the surface screen

        Returns
        -------
        monster_x: int
            the x coordinate of the current position of the monster
        monster_y: int
            the y coordinate of the current position of the monster

        """

        self.x = x
        self.y = y

        # 'stick' the image to the screen at the given position
        surface.blit(image,(self.x,self.y))

        # define the direction that monster can go
        move_list = ['left','right','up','down']

        # we will define two types of movement by choosing a random number
        random_number = random.random()
        # the bot has 75% to make the biased move, which is, do the same movement again
        # this is the biased move
        if random_number < 0.75 and self.last_move != None:
            movement = self.last_move
            self.last_move = movement
        # this is the unbiased move
        else:
            movement = random.choice(move_list)
            self.last_move = movement
        # decide which direction to go
        if movement == 'left':
            if self.x > vel:
                self.x -= vel
            # if the bot is gonna touch the wall, let it move to the opposite direction
            else:
                self.x += vel
                self.last_move = 'right'
        if movement == 'right':
            if self.x < screen_width - self.width - vel:
                self.x += vel
            else:
                self.x -= vel
                self.last_move = 'left'
        if movement == 'up':
            if self.y > vel:
                self.y -= vel
            else:
                self.y += vel
                self.last_move = 'down'
        if movement == 'down':
            if self.y < screen_height - self.height - vel:
                self.y += vel
            else:
                self.y -= vel
                self.last_move = 'up'

        # return the updated position
        return self.x, self.y

    def kill_or_not(self,player):
        """ Decide whether the player is killed by the monster

        We are going to achieve this simply by deciding, whether one of the four
        vertexes of the monster is in the region that the player located in.
        Thus, we will use if statement four times, if any on of the statement is
        True, the player is killed by the monster.

        Parameters
        ----------
        player:   Player
            the player object show in the game

        Returns
        -------
        bool
            whether player is killed by the monster in this loop

        """


        if player.bot_x < self.x < player.bot_x + player.width and player.bot_y < self.y < player.bot_y + player.height:
            return True
        if player.bot_x < self.x + self.width < player.bot_x + player.width and player.bot_y < self.y + self.height < player.bot_y + player.height:
            return True
        if player.bot_x < self.x + self.width < player.bot_x + player.width and player.bot_y < self.y < player.bot_y + player.height:
            return True
        if player.bot_x < self.x < player.bot_x + player.width and player.bot_y < self.y + self.height < player.bot_y + player.height:
            return True
        return False


# this class is the food that Player need to eat to gain score
class Food_to_eat():
    """ Food_to_eat class defines the food(a tiny dot), that the player
        need to eat to gain score.

        Args:
            color: Color
                the color of the dot
            radius: int
                the radius of the dot

        Attributes:
            color: Color
                the color of the dot
            radius: int
                the radius of the dot
            x:   int
                the x coordinate of the food
            y:   int
                the y coordinate of the food

        Methods:
            show():
                show the food on the screen
            eat_or_not():
                to decide whether the food is eaten by the player

    """

    # food is a circle shaped dot that has a radius
    def __init__(self, color = (255,255,255), radius = 5):
        self.color = color
        self.radius = radius
        self.x = 0
        self.y = 0

    # this method will show the food at the given position,
    # this position will be decided by random in the game loop
    def show(self,surface,rand_x,rand_y):
        """ this method will show the food at the given position
        the position of the food will be randomly decided

        Parameters
        ----------
        surface:
            the window that the food will be diplayed on
        rand_x:
            the x coordinate that the food will be centered at
        rand_y:
             the y coordinate that the food will be centered at

        Returns
        -------
        No returns

        """

        # draw the foods
        pygame.draw.circle(surface,self.color,(rand_x,rand_y),self.radius)
        self.x = rand_x
        self.y = rand_y

    def eat_or_not(self,player):
        if player.bot_x + player.width >self.x> player.bot_x and player.bot_y + player.height > self.y > player.bot_y:
            return True
