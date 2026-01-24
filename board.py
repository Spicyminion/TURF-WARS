import pygame
from layout import layout, TileType
from tile import Tile, Building, Button
from constants import DIMENSION

#class BoardState()


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

    def draw(self, camera):
        for column in range(len(layout)):
            for row in range(len(layout[column])):
                rotation = camera.rotation_offset
                if rotation == 1:
                    column_rot = row
                    row_rot = DIMENSION - 1 - column
                elif rotation == 2:
                    column_rot = DIMENSION - 1 - column
                    row_rot = DIMENSION - 1 - row
                elif rotation == 3:
                    column_rot = DIMENSION - 1 - row
                    row_rot = column
                else:
                    column_rot = column
                    row_rot = row

                    tile = self.board.tiles[column_rot][row_rot]
                    img = self.local_imgs[tile.img_key]

                    x = (
                            self.INITIAL_OFFSET_X
                            + (self.HALF_WIDTH * column)
                            - (self.HALF_WIDTH * row)
                    )
                    y = (
                            self.INITIAL_OFFSET_Y +
                            (self.HALF_HEIGHT * column) +
                            (self.HALF_HEIGHT * row)
                    )

                    self.window.blit(img, (x, y))



#class Board


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



