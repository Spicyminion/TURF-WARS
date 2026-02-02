from cgi import print_form

import pygame
from pygame.examples.scroll import zoom_factor

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

    def center_board(self):
        self.x_offset = 0
        self.y_offset = 0
        self.rotation_offset = 0
        self.zoom_level = 1.0
        self.move_camera()

    def rotate_point_cw(self, x, y, cx, cy, turns, half_width, half_height):
        """
        Rotate point (x, y) clockwise around pivot (cx, cy)
        in isometric space.
        """
        turns %= 4
        rx, ry = x, y
        if turns == 0:
            return rx, ry

        # aspect ratio correction (diamond space → square space)
        ratio = half_width / half_height

        # move to origin (pivot)
        dx = x - cx
        dy = (y - cy) * ratio

        # rotate in square space
        if turns == 1:        # 90° CW
            rx, ry = -dy, dx
        elif turns == 2:      # 180°
            rx, ry = -dx, -dy
        elif turns == 3:      # 270° CW
            rx, ry = dy, -dx

        # undo aspect ratio
        ry /= ratio

        # move back from origin
        return cx + rx, cy + ry

    def game_to_camera(self, gx, gy):
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        # Rotate around screen center
        rx, ry = self.rotate_point_cw(
            gx, gy,
            center_x, center_y,
            self.rotation_offset,
            self.config.HALF_WIDTH,
            self.config.HALF_HEIGHT
        )

        # Apply camera translation (pan)
        tx = rx + self.x_offset
        ty = ry + self.y_offset

        # Zoom around screen center
        zx = center_x + (tx - center_x) * self.zoom_level
        zy = center_y + (ty - center_y) * self.zoom_level

        # Convert image center -> top-left for blitting
        screen_x = zx - (self.config.HALF_WIDTH * self.zoom_level)
        screen_y = zy - (self.config.HALF_HEIGHT * self.zoom_level)

        return screen_x, screen_y

    def camera_to_game(self, screen_x, screen_y):
        print(f"ORIG: {screen_x}, {screen_y}")
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        # Top-left -> image center
        zx = screen_x #+ self.config.HALF_WIDTH
        zy = screen_y #+ self.config.HALF_HEIGHT

        # Undo zoom
        tx = center_x + ((zx - center_x) / self.zoom_level)
        ty = center_y + ((zy - center_y) / self.zoom_level)
        print(f"TX, TY: {tx}, {ty}")
        # Undo translation (pan)
        rx = tx - self.x_offset
        ry = ty - self.y_offset
        print(f"NON ROT {rx}, {ry}")
        # Undo rotation (rotate CCW)
        gx, gy = self.rotate_point_cw(
            rx, ry,
            center_x, center_y,
            4 - self.rotation_offset, #self.rotation_offset,
            self.config.HALF_WIDTH,
            self.config.HALF_HEIGHT
        )

        cx = gx - self.config.INITIAL_OFFSET_X  - self.config.HALF_WIDTH
        cy = gy - self.config.INITIAL_OFFSET_Y
        print(f"FINAL: {gx}, {gy}")
        print(f"CENT: {cx}, {cy}")
        return gx, gy












