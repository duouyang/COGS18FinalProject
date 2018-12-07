from Robot import Bot, Player, Monster
import pygame

def test_Bot():
    assert isinstance(Bot(5,10), Bot)

def test_Bot_width():
    test_bot = Bot(10,20)
    assert test_bot.width == 10
