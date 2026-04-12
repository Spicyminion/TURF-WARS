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
    def __init__(self, col, row, type, id):
        self.row = row
        self.col = col
        self.type = type
        self.id = id

class Character:
    def __init__(self, col, row, health):
        self.row = row
        self.col = col
        self.health = health


