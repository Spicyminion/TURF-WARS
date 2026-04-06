import pygame
from constants import COLOR_KEY
from layout import TileType, TILETYPE_TO_SPRITE
#import constants

class Tile:
    def __init__(self, type, col, row):
        self.row = row
        self.col = col
        self.type = type
        self.img_key = TILETYPE_TO_SPRITE[type]
        self.characters = []
        self.building = None

class Building:
    def __init__(self, col, row, config, type):
        self.row = row
        self.col = col
        self.type = type


class Button:
    def __init__(self, x, y, command):
        self.x = x
        self.y = y
        self.command = command

    def get_rect(self):
        return self.x, self.y

    def on_click(self):
        self.command.execute()


