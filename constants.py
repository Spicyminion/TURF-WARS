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

###################################
# DIMENSIONS FOR BOARD AND SCREEN #
###################################

INTERNAL_WIDTH, INTERNAL_HEIGHT = 1800, 900 # tested on desktop monitor
SCREEN_WIDTH, SCREEN_HEIGHT = INTERNAL_WIDTH, INTERNAL_HEIGHT  # 1800, 900

SCALE_FACTOR = 1

BLOCK_SCALE_FACTOR = 4.0  # usual final tile size will 196w x 100h (4.0)
HALF_HEIGHT = 12 * BLOCK_SCALE_FACTOR  # offset dim (half of diamond)
HALF_WIDTH =  25 * BLOCK_SCALE_FACTOR  # offset dim (half of width)
DIMENSION = 7

INITIAL_OFFSET_X = SCREEN_WIDTH / 2 - HALF_WIDTH
INITIAL_OFFSET_Y = (SCREEN_HEIGHT / 2) - (HALF_HEIGHT * 2 * DIMENSION / 2)  # first div brings to mid, 2nd moves up height of half of board

##############
# PNG ASSETS #
##############

COLOR_KEY = (0,0,0)
def load_image(img, scale_factor):
    load = pygame.image.load(img)
    w, h = load.get_size()
    load = pygame.transform.scale(load, (int(w * SCALE_FACTOR), int(h * SCALE_FACTOR)))
    return load

BLOCK = pygame.image.load('grass_block.png')
CLICKED_BLOCK = pygame.image.load('clicked_grass_block.png')
APARTMENT = pygame.image.load('pixil-layer-Layer_5.png')

w, h = BLOCK.get_size()

BLOCK.set_colorkey(COLOR_KEY)
CLICKED_BLOCK.set_colorkey(COLOR_KEY)
APARTMENT.set_colorkey(COLOR_KEY)

BLOCK = pygame.transform.scale(BLOCK, (int(w * BLOCK_SCALE_FACTOR), int(h * BLOCK_SCALE_FACTOR)))
CLICKED_BLOCK = pygame.transform.scale(CLICKED_BLOCK, (int(w * BLOCK_SCALE_FACTOR), int(h * BLOCK_SCALE_FACTOR)))
APARTMENT = pygame.transform.scale(APARTMENT, (int(w * 2), int(h * 2)))

BLOCK_MASK = pygame.mask.from_surface(BLOCK)
CLICKED_BLOCK_MASK = pygame.mask.from_surface(CLICKED_BLOCK)

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


