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

        # 1) Rotate around screen center
        rx, ry = self.rotate_point_cw(
            gx, gy,
            center_x, center_y,
            self.rotation_offset,
            self.config.HALF_WIDTH,
            self.config.HALF_HEIGHT
        )

        # 2) Apply camera translation (pan)
        tx = rx + self.x_offset
        ty = ry + self.y_offset

        # 3) Zoom around screen center
        zx = center_x + (tx - center_x) * self.zoom_level
        zy = center_y + (ty - center_y) * self.zoom_level

        # 4) Convert image center → top-left for blitting
        screen_x = zx - self.config.HALF_WIDTH
        screen_y = zy - self.config.HALF_HEIGHT

        return screen_x, screen_y

    def camera_to_game(self, screen_x, screen_y):
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        # 1) Top-left → image center
        zx = screen_x + self.config.HALF_WIDTH
        zy = screen_y + self.config.HALF_HEIGHT

        # 2) Undo zoom
        tx = center_x + (zx - center_x) / self.zoom_level
        ty = center_y + (zy - center_y) / self.zoom_level

        # 3) Undo translation (pan)
        rx = tx - self.x_offset
        ry = ty - self.y_offset

        # 4) Undo rotation (rotate CCW)
        gx, gy = self.rotate_point_cw(
            rx, ry,
            center_x, center_y,
            -self.rotation_offset,
            self.config.HALF_WIDTH,
            self.config.HALF_HEIGHT
        )

        return gx , gy


'''
    def rotate_cw(self, x, y, distance_x, distance_y, turns):
        turns %= 4
        if turns == 0:
            return x, y

        # True diamond ratio (width / height)
        ratio = self.config.HALF_WIDTH / self.config.HALF_HEIGHT

        # --- normalize into square space ---
        nx = distance_x
        ny = distance_y * ratio

        # rotate in square space (for some reason rotation needs to be reversed for isometric)
        if turns == 3:  # (270)
            rx = ny
            ry = -nx
        elif turns == 2:  # (180)
            rx = -nx
            ry = -ny
        elif turns == 1:  # CW (90)
            rx = -ny
            ry = nx
        else:
            return x, y

        ry /= ratio


        x_rot = x + (rx - distance_x) # subtracting distance_x/y brings x/y to center of screen before rotating
        y_rot = y + (ry - distance_y)

        return x_rot, y_rot  # this is returning the magnitude (need to move to center of board)

    def game_to_camera(self, img_x, img_y):

        # First rotate around center of screen
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        distance_x = img_x - center_x   # distance from center of board
        distance_y = img_y - center_y

        shift_x, shift_y = self.rotate_cw(
            img_x, img_y,
            distance_x, distance_y,
            self.rotation_offset
        )

        # Now apply NSEW translation
        translate_x = shift_x + self.x_offset
        translate_y = shift_y + self.y_offset

        # Apply zoom and center (remember zoom is from the origin of the board)
        screen_x = center_x + (translate_x - center_x) * self.zoom_level
        screen_y = center_y + (translate_y - center_y) * self.zoom_level
        
        return screen_x - self.config.HALF_WIDTH, screen_y - self.config.HALF_HEIGHT

    def camera_to_game(self, screen_x, screen_y):

        # 1) move into screen-centered space
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        shifted_x = screen_x - center_x # + self.config.HALF_WIDTH  # remember coord stored in tiles is in the center
        shifted_y = screen_y - center_y # + self.config.HALF_HEIGHT

        # undo zoom (larger the zoom, the smaller the distance from center you're clicking)
        shifted_x /= self.zoom_level
        shifted_y /= self.zoom_level

        # undo camera translation
        distance_x = shifted_x - self.x_offset
        distance_y = shifted_y - self.y_offset

        # rotate around screen-centered world pivot (inverse)
        rotate = 4 - self.rotation_offset
        shifted_x, shifted_y = self.rotate_cw(center_x + distance_x, center_y + distance_y, distance_x, distance_y, rotate)

        shifted_x -= self.x_offset  # final subtraction is to center rotated coords
        shifted_y -= self.y_offset

        print(f"SHIFTED_X:{shifted_x} SHIFTED_Y:{shifted_y}")
        return shifted_x, shifted_y
'''











