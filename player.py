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

    def rotate_cw(self, x, y, distance_x, distance_y, turns):
        # turns %= 4
        if turns == 0:
            return x, y

        # True diamond ratio (width / height)
        ratio = self.config.HALF_WIDTH / self.config.HALF_HEIGHT

        # --- normalize into square space ---
        nx = distance_x
        ny = distance_y * ratio

        # rotate in square space (for some reason rotation needs to be reversed for isometric)
        if turns == 3:  # 90° CW
            rx = ny
            ry = -nx
        elif turns == 2:  # 180°
            rx = -nx
            ry = -ny
        elif turns == 1:  # 270° CW
            rx = -ny
            ry = nx
        else:
            return x, y

        ry /= ratio


        x_rot = x + (rx - distance_x) # subtracting distance_x/y zeros to center before rotating
        y_rot = y + (ry - distance_y)

        return x_rot, y_rot

    def game_to_camera(self, img_x, img_y):

        # First rotate around center of screen
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        distance_x = img_x - center_x
        distance_y = img_y - center_y

        shift_x, shift_y = self.rotate_cw(
            img_x, img_y,
            distance_x, distance_y,
            self.rotation_offset
        )

        # Now apply NSEW translation
        translate_x = shift_x + self.x_offset
        translate_y = shift_y + self.y_offset

        # Apply zoom (remember zoom is from the origin of the board)
        screen_x = center_x + (translate_x - center_x) * self.zoom_level
        screen_y = center_y + (translate_y - center_y) * self.zoom_level

        return screen_x - self.config.HALF_WIDTH, screen_y - self.config.HALF_HEIGHT

    '''
    def game_to_camera(self, img_x, img_y):
        # 1) rotate around screen-centered world pivot
        pivot_x = -self.x_offset
        pivot_y = -self.y_offset

        shifted_x, shifted_y = self.rotate_cw(img_x - pivot_x, img_y - pivot_y, self.rotation_offset)
        shifted_x += pivot_x
        shifted_y += pivot_y

        # 2) apply camera translation
        shifted_x -= self.x_offset
        shifted_y -= self.y_offset

        # 3) apply zoom
        shifted_x *= self.zoom_level
        shifted_y *= self.zoom_level

        # 4) move back to screen space
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2

        screen_x = shifted_x + center_x
        screen_y = shifted_y + center_y

        return screen_x, screen_y
    '''
    def camera_to_game(self, screen_x, screen_y):
        # 1) move into screen-centered space
        center_x = self.config.screen_width / 2
        center_y = self.config.screen_height / 2
        shifted_x = screen_x - center_x
        shifted_y = screen_y - center_y

        # 2) undo zoom
        shifted_x /= self.zoom_level
        shifted_y /= self.zoom_level

        # 3) undo camera translation
        shifted_x += self.x_offset
        shifted_y += self.y_offset

        # 4) rotate around screen-centered world pivot (inverse)
        pivot_x = -self.x_offset
        pivot_y = -self.y_offset
        shifted_x, shifted_y = self.rotate_cw(shifted_x - pivot_x, shifted_y - pivot_y, self.rotation_offset)
        shifted_x += pivot_x
        shifted_y += pivot_y

        return shifted_x, shifted_y

    def center_board(self):
        self.x_offset = 0
        self.y_offset = 0
        self.rotation_offset = 0
        self.zoom_level = 1.0
        self.move_camera()








