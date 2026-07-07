import pygame
from constants import COLOR_KEY
from layout import TileType, TILETYPE_TO_SPRITE
#import constants

class Tile:
    def __init__(self, type, col, row, x, y):
        self.row = row
        self.col = col
        self.type = type
        self.img_key = TILETYPE_TO_SPRITE[type]
        self.x = x
        self.y = y
        self.characters = []
        self.building = None
        self.id = None

    def check_click(self, click_x, click_y):
        check = True
        for character in self.characters:
            if character.check_click(click_x, click_y):
                check = False
                break
        if check:
            for building in self.building:
                if building.check_click(click_x, click_y):
                    print("building clicked!")
                    break

class Building:
    def __init__(self, col, row, config, type, id):
        self.row = row
        self.col = col
        self.config = config
        self.type = type
        self.img = self.config.assets.imgs['apartment']
        self.id = id
        self.revenue = 100

    def generate_money(self):
        print("printing money WOOO!!!")
        return self.revenue







