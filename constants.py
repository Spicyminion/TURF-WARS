import pygame
from enum import Enum

# TILE TYPES

class TileType(Enum):
    BLANK = 0
    BASE = 1
    SPAWN_CIRCLE = 2
    LOCK_SPACE = 3
    HOUSE = 4
    MALL = 5


# DIMENSIONS FOR BOARD AND SCREEN
SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 900

SCALE_FACTOR = 4.0
HALF_HEIGHT = 12 * SCALE_FACTOR  # offset dim (half of diamond)
HALF_WIDTH =  25 * SCALE_FACTOR  # offset dim (half of width)
DIMENSION = 7

INITIAL_OFFSET_X = SCREEN_WIDTH / 2 - HALF_WIDTH
INITIAL_OFFSET_Y = (SCREEN_HEIGHT / 2) - (HALF_HEIGHT * 2 * DIMENSION / 2)  # first div brings to mid, 2nd moves up height of half of board

# PNG ASSETS
BLOCK = pygame.image.load('grass_block.png')
CLICKED_BLOCK = pygame.image.load('clicked_grass_block.png')
COLOR_KEY = (0,0,0)
w, h = BLOCK.get_size()

BLOCK.set_colorkey(COLOR_KEY)
CLICKED_BLOCK.set_colorkey(COLOR_KEY)

BLOCK = pygame.transform.scale(BLOCK, (int(w * SCALE_FACTOR), int(h * SCALE_FACTOR)))
CLICKED_BLOCK = pygame.transform.scale(CLICKED_BLOCK, (int(w * SCALE_FACTOR), int(h * SCALE_FACTOR)))

'''
def load_assets():
    global BLOCK, CLICKED_BLOCK
    COLOR_KEY = (0,0,0)
    block = pygame.image.load('grass_block.png').convert()
    clicked_block = pygame.image.load('clicked_grass_block.png').convert()
    w, h = block.get_size()

    block.set_colorkey(COLOR_KEY)
    clicked_block.set_colorkey(COLOR_KEY)

    BLOCK = pygame.transform.scale(block,(int(w * SCALE_FACTOR), int(h * SCALE_FACTOR)))
    CLICKED_BLOCK = pygame.transform.scale(clicked_block,(int(w * SCALE_FACTOR), int(h * SCALE_FACTOR)))
'''


