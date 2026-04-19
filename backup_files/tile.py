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
    def __init__(self, col, row, config, type,
                 tile_x, tile_y, tile_width, tile_height):
        self.row = row
        self.col = col
        self.config = config
        self.type = type
        self.img = self.config.assets.imgs['apartment']
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.w, self.h = self.img.get_size()
        self.x = tile_x - (self.w/2)
        self.y = tile_y - (self.h/2)
        self.draw_x = tile_x + self.tile_width - (self.w / 2)
        self.draw_y = tile_y + self.tile_height - (self.h / 2)

    def draw_coords(self, x, y):
        draw_x = x - self.w/2
        draw_y = y - self.h/2
        return draw_x, draw_y
    ''' 
    def draw_building(self, window, tile_height, tile_width, tile_x, tile_y):
        draw_x, draw_y = self.get_coord(tile_x, tile_y, tile_width, tile_height)
        window.blit(self.img, (draw_x, draw_y))

    def check_click(self, tile_height, tile_width, tile_x, tile_y):  # workaround for coordinate logic
        build_x, build_y = self.get_coord(tile_x, tile_y, tile_width, tile_height, tile_width)

    def draw_stat(self, window, x, y):
        test = self.config.assets.get('test_stat')
        w, h = self.rect.w, self.rect.h
        x, y = self.rect.x + w/2 - test.get_size()[0] / 2, self.rect.y
        window.blit(test, (x, y))
    '''



class Button:
    def __init__(self, x, y, command):
        self.x = x
        self.y = y
        self.command = command

    def get_rect(self):
        return self.x, self.y

    def on_click(self):
        self.command.execute()


