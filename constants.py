import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 900

SCALE_FACTOR = 4.0
HALF_HEIGHT = 12 * SCALE_FACTOR  # offset dim (half of diamond)
HALF_WIDTH =  25 * SCALE_FACTOR  # offset dim (half of width)
DIMENSION = 7

INITIAL_OFFSET_X = SCREEN_WIDTH / 2 - HALF_WIDTH
INITIAL_OFFSET_Y = (SCREEN_HEIGHT / 2) - (HALF_HEIGHT * 2 * DIMENSION / 2)  # first div brings to mid, 2nd moves up height of half of board