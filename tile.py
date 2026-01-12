import pygame
from constants import SCALE_FACTOR, HALF_HEIGHT, HALF_WIDTH, BLOCK, CLICKED_BLOCK, TileType, INITIAL_OFFSET_Y, INITIAL_OFFSET_X
#import constants

class Tile:

    def __init__(self, type, x, y):
        self.x = x
        self.y = y
        self.type = type
        self.characters = []

    def draw(self, window):
        if self.type == TileType.BLANK:
            window.blit(BLOCK, (self.x, self.y))
        else:
            window.blit(CLICKED_BLOCK, (self.x, self.y))


