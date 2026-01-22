import pygame
from pygame.examples.scroll import zoom_factor
from scipy.signal import zoom_fft

from layout import layout, TileType
from constants import DIMENSION, HALF_HEIGHT


class Player:

    def __init__(self, player_id):
        self.id = player_id
        self.money = 200


class PlayerCamera:

    def __init__(self, player, window, config, board, initial_x_offset, initial_y_offset, half_width, half_height):
        self.zoom_level = 1.0
        self.rotate = 0
        self.player = player
        self.window = window
        self.config = config
        self.board = board
        self.initial_x_offset = initial_x_offset
        self.initial_y_offset = initial_y_offset
        self.initial_half_width = half_width
        self.initial_half_height = half_height
        self.INITIAL_OFFSET_X = initial_x_offset
        self.INITIAL_OFFSET_Y = initial_y_offset
        self.HALF_WIDTH = half_width
        self.HALF_HEIGHT = half_height
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.camera_rotation_offset = 0 # 1 = 90 deg, 2 = 180, 3 = 270
        self.board_center = (self.config.screen_width / 2) + (self.config.screen_height / 2) # start at true center of board
        self.local_imgs = {}
        self.img_masks = {}

        for name,img in self.config.assets.imgs.items():
            self.local_imgs[name] = img
        self.update_masks()

    def draw(self, window, img, x, y):
        window.blit(img, (x, y))  # print where top left of rectangle is

    def game_to_camera(self, x, y):
        pass

    def camera_to_game(self, x, y):

        x = (x * zoom_factor) + self.camera_offset_x
        y = (y * zoom_factor) + self.camera_offset_y

        return x, y

    def draw_all(self):

        for col in range(len(layout)):
            for row in range(len(layout[col])):

                if self.camera_rotation_offset == 1:
                    col_rot = row
                    row_rot = DIMENSION - 1 - col
                elif self.camera_rotation_offset == 2:
                    col_rot = DIMENSION - 1 - col
                    row_rot = DIMENSION - 1 - row
                elif self.camera_rotation_offset == 3:
                    col_rot = DIMENSION - 1 - row
                    row_rot = col
                else:
                    col_rot = col
                    row_rot = row

                tile = self.board.tiles[col_rot][row_rot]
                img = self.local_imgs[tile.img_key]

                x = (
                        self.INITIAL_OFFSET_X
                        + (self.HALF_WIDTH * col)
                        - (self.HALF_WIDTH * row)
                )
                y = (
                        self.INITIAL_OFFSET_Y +
                        (self.HALF_HEIGHT * col) +
                        (self.HALF_HEIGHT * row)
                )

                self.window.blit(img, (x, y))

                for struct in tile.building:
                    img = self.local_imgs['Apartment-1b']
                    w, h = img.get_size()
                    build_x = x + self.HALF_WIDTH - w/2
                    build_y = y + self.HALF_HEIGHT - h/2
                    self.window.blit(img, (build_x, build_y))

        for button in self.board.buttons:
            img = self.local_imgs['apartment']
            self.window.blit(img, (button.x, button.y))


    def update_imgs(self):
        for name, img in self.config.assets.imgs.items():
            w, h = img.get_size()
            img = pygame.transform.scale(img, (round(w * self.zoom_level), round(h * self.zoom_level)))
            self.local_imgs[name] = img
        self.HALF_WIDTH =  self.initial_half_width * self.zoom_level
        self.HALF_HEIGHT = self.initial_half_height * self.zoom_level
        self.INITIAL_OFFSET_X = ((
                                self.config.screen_width / 2)
                                 - self.HALF_WIDTH
                                 + self.camera_offset_x
                                 )
        self.INITIAL_OFFSET_Y = (
                                (self.config.screen_height / 2)
                                - (self.HALF_HEIGHT * 2 * DIMENSION / 2)  +
                                 self.camera_offset_y
                                ) # first div brings to mid, 2nd moves up height of half
        #self.draw_all()

    def update_masks(self):
        for name, img in self.local_imgs.items():
            mask = pygame.mask.from_threshold(img, (0, 0, 0), (1, 1, 1, 255))
            mask.invert()
            self.img_masks[name] = mask

    def convert_click(self, x, y):
        pass

    def center_board(self):
        self.HALF_WIDTH = self.initial_half_width
        self.HALF_HEIGHT = self.initial_half_height
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.camera_rotation_offset = 0
        self.zoom_level = 1.0
        self.update_masks()
        self.update_imgs()
        #self.draw_all()

    def calculate_position(self, x, y):

        # First check if a button is clicked, if not, then check if a tile is clicked

        for button in self.game.UI:
            img = self.local_imgs['apartment']
            rect = img.get_rect(topleft=(button.x, button.y))
            mask = self.img_masks['apartment']
            if rect.collidepoint(x, y):
                check_x, check_y = x - button.x, y- button.y
                if mask.get_at((check_x, check_y)):
                    print("button clicked!")

        # Recenter to remove any visual adjustments (zoom, rotation, camera movement)
        cx, cy = x - self.INITIAL_OFFSET_X - self.HALF_WIDTH, y - self.INITIAL_OFFSET_Y
        #cx, cy = x - self.INITIAL_OFFSET_X, y - self.INITIAL_OFFSET_Y

        # Now normalize x & y coords to width and height of each tile respectively (units for moving)
        nx = cx / self.HALF_WIDTH
        ny = cy / self.HALF_HEIGHT

        # Next convert into x, y within range of (6,6) 7x7 tiles (0-based idx)
        gx = (nx + ny) / 2
        gy = (ny - nx) / 2

        # Compute which tile is being used
        col = int(gx)
        row = int(gy)

        if 0 <= col <= (DIMENSION - 1) and 0 <= row <= (DIMENSION - 1):

            tile_x = self.INITIAL_OFFSET_X + (self.HALF_WIDTH * col) - self.HALF_WIDTH * row
            tile_y = self.INITIAL_OFFSET_Y + (self.HALF_HEIGHT * col) + self.HALF_HEIGHT * row
            image = self.local_imgs['grass_block']              # every tile will have the same mask
            rect = image.get_rect(topleft=(tile_x, tile_y))     # create a rectangle from the top left coord of the image (treat as x,y)
            mask = self.img_masks['grass_block']                # mask is inside a rect starting from 0,0 top left
            print(f"x, y:{x, y} | tile_origin:{tile_x, tile_y}")
            #mask.invert()
            if not rect.collidepoint(x, y):  # check if clicked inside where the rect is (in realspace)
                print("nope")
                return False
            check_x, check_y = (x - tile_x, y - tile_y)  # recenter around top_L 0,0
            if self.camera_rotation_offset == 1:
                col, row = row, DIMENSION - 1 - col
            elif self.camera_rotation_offset == 2:
                col = DIMENSION - 1 - col
                row = DIMENSION - 1 - row
            elif self.camera_rotation_offset == 3:
                col, row = DIMENSION - 1 - row, col
            return col, row, mask.get_at((round(check_x), round(check_y)))  # check if the click is within the boundaries of the image

        else:
            return None






