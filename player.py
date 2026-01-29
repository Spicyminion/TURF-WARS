import pygame
from pygame.examples.scroll import zoom_factor
from pygame.pypm import Initialize
from scipy.signal import zoom_fft

from layout import layout, TileType
from constants import DIMENSION, HALF_HEIGHT


class Player:

    def __init__(self, player_id, window):
        self.id = player_id
        self.money = 200
        self.camera = PlayerCamera


class PlayerCamera:
    def __init__(self, config):
        self.zoom_level = 1.0
        self.config = config
        self.OFFSET_X = self.config.INITIAL_OFFSET_X
        self.OFFSET_Y = self.config.INITIAL_OFFSET_Y
        self.y_offset = 0
        self.x_offset = 0
        self.rotation_offset = 0 # 1 = 90 deg, 2 = 180, 3 = 270

    def move_camera(self):
        half_width = self.config.HALF_WIDTH * self.zoom_level
        half_height = self.config.HALF_HEIGHT * self.zoom_level
        self.OFFSET_X = (
                (self.config.screen_width / 2)
                 - half_width
                 + self.x_offset
        )
        self.OFFSET_Y = (
                (self.config.screen_height / 2)
                - (half_height * 2 * DIMENSION / 2) +
                self.y_offset
        )

    def game_to_camera(self, x, y):
        x = x - self.x_offset
        y = y - self.y_offset
        return x, y

    def camera_to_game(self, x, y):
        x = x - self.x_offset
        y = y - self.y_offset

        return x, y

    def center_board(self):
        self.x_offset = 0
        self.y_offset = 0
        self.rotation_offset = 0
        self.zoom_level = 1.0
        self.move_camera()








