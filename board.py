import pygame
from layout import layout
from tile import Tile
#from constants import

class Board:

    def __init__(self, window, config):
        self.window = window
        self.config = config
        self.tiles = []
        self.define_grid()

    def define_grid(self):
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                x = self.config.INITIAL_OFFSET_X + (self.config.HALF_WIDTH * column) - self.config.HALF_WIDTH * row
                y = self.config.INITIAL_OFFSET_Y + (self.config.HALF_HEIGHT * column) + self.config.HALF_HEIGHT * row
                self.tiles[column].append(Tile(tile_type, x, y, column, row, self.config))

    def draw_board(self, window):
        for column_tiles in self.tiles:
            for tile in column_tiles:
                tile.draw(window)

    def rotate_board(self):
        print("hi")
        # do something
        #self.draw_board(self, window)

