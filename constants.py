import pygame
from enum import Enum

###################################
# DIMENSIONS FOR BOARD AND SCREEN #
###################################

#INTERNAL_WIDTH, INTERNAL_HEIGHT = 1800, 900 # tested on desktop monitor
#SCREEN_WIDTH, SCREEN_HEIGHT = INTERNAL_WIDTH, INTERNAL_HEIGHT  # 1800, 900

SCALE_FACTOR = 1
BLOCK_SCALE = 4.0   # usual final tile size will 196w x 100h (4.0)
HALF_HEIGHT = 12 * BLOCK_SCALE  # offset dim (half of diamond)
HALF_WIDTH =  25 * BLOCK_SCALE  # offset dim (half of width)
DIMENSION = 7
COLOR_KEY = (0,0,0)
##############
# PNG ASSETS #
##############



