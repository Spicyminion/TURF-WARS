import pygame
from layout import layout, TileType, BuildType
from server_tile import Tile, Building, Button
from constants import DIMENSION

#class BoardState()

class Board:

    def __init__(self):
        self.tiles = []
        self.define_grid()

    def define_grid(self):
        id = 0
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                #if column == 0 and row == 0:
                #    print(f"ORIG TILE_X{x} ORIG TILE_Y{y}")
                self.tiles[column].append(Tile(tile_type, column, row)) # true center
                id += 1
                if column == 1 and row == 1:
                    tile = self.tiles[column][row]
                    tile.building = Building(column, row, BuildType.APARTMENT)

    def game_to_tile(self, x, y):
        pass




