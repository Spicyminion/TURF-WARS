import pygame
from layout import layout
from tile import Tile
from constants import HALF_HEIGHT, HALF_WIDTH, INITIAL_OFFSET_Y, INITIAL_OFFSET_X, BLOCK, CLICKED_BLOCK

class Board:

    def __init__(self, window):
        self.window = window
        self.tiles = []
        self.define_grid()

    def define_grid(self):
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                x = INITIAL_OFFSET_X + (HALF_WIDTH * column) - HALF_WIDTH * row
                y = INITIAL_OFFSET_Y + (HALF_HEIGHT * column) + HALF_HEIGHT * row
                self.tiles[column].append(Tile(tile_type, x, y, column, row))

    def draw_board(self, window):
        for column_tiles in self.tiles:
            for tile in column_tiles:
                tile.draw(window)

    def rotate_board(self):
        print("hi")
        # do something
        #self.draw_board(self, window)

