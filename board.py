import pygame
from layout import layout, TileType
from tile import Tile, Building
#from constants import

class Board:

    def __init__(self, window, config):
        self.window = window
        self.config = config
        self.tiles = []
        self.define_grid()

    def define_grid(self):
        id = 0
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                self.tiles[column].append(Tile(tile_type, column, row))
                id += 1
                if column == 1 and row == 1:
                    tile = self.tiles[column][row]
                    tile.building.append(Building(column, row, self.config))


class UI:
    def __init__(self):
        self.buttons = []

    def check_buttons(self, x, y):
        for button in self.buttons:
            if button.check_click(x, y):
                break

    def draw_buttons(self, window):
        for button in self.buttons:
            button.draw(window)



