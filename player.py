import pygame
from pygame.examples.scroll import zoom_factor
from scipy.signal import zoom_fft

from layout import layout, TileType
from constants import DIMENSION

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

    def draw(self, window, img, x, y):
        window.blit(img, (x, y))  # print where top left of rectangle is

    def draw_all(self):
        for column in range(len(layout)):
            for row in range(len(layout[column])):
                x = self.INITIAL_OFFSET_X + (self.HALF_WIDTH * column) - self.HALF_WIDTH * row
                y = self.INITIAL_OFFSET_Y + (self.HALF_HEIGHT * column) + self.HALF_HEIGHT * row
                tile = self.board.tiles[row][column]
                if tile.type == TileType.BLANK:
                    img = self.local_imgs['grass_block']
                else:
                    img = self.local_imgs['clicked_block']
                self.window.blit(img, (x, y))


    def update_imgs(self):
        for name, img in self.config.assets.imgs.items():
            w, h = img.get_size()
            img = pygame.transform.scale(img, (round(w * self.zoom_level), round(h * self.zoom_level)))
            self.local_imgs[name] = img
        self.HALF_WIDTH =  self.initial_half_width * self.zoom_level
        self.HALF_HEIGHT = self.initial_half_height * self.zoom_level
        self.INITIAL_OFFSET_X = (self.config.screen_width / 2) - self.HALF_WIDTH + self.camera_offset_x
        self.INITIAL_OFFSET_Y = ((self.config.screen_height / 2) -
                                 (self.HALF_HEIGHT * 2 * DIMENSION / 2)  +
                                 self.camera_offset_y) # first div brings to mid, 2nd moves up height of half
        self.draw_all()

    def update_masks(self):
        for name, img in self.local_imgs.items():
            mask = pygame.mask.from_threshold(img, (0, 0, 0), (1, 1, 1, 255))
            mask.invert()
            self.img_masks[name] = mask


    def check_click(self, row, col, x, y):
        rect =
        if not self.rect.collidepoint(click_x, click_y):  # check if clicked inside where the rect is (in realspace)
            return False
        check_x, check_y = (click_x - self.rect.x, click_y - self.rect.y)  # recenter around top_L 0,0
        # print(check_x, check_y)
        return self.mask.get_at((check_x, check_y))  # check if the click is within the boundaries of the image

    def convert_click(self, x, y):
        pass

    def calculate_position(self, x, y):
        # Recenter to remove any visual adjustments (zoom, rotation, camera movement)
        cx, cy = x - self.INITIAL_OFFSET_X - self.HALF_WIDTH, y - self.INITIAL_OFFSET_Y

        # Now normalize x & y coords to width and height of each tile respectively (units for moving)
        nx = cx / self.HALF_WIDTH
        ny = cy / self.HALF_HEIGHT

        # Next convert into x, y within range of (7,7) 7x7 tiles
        gx = (nx + ny) / 2
        gy = (ny - nx) / 2

        # Compute which tile is being used
        col = int(gx)
        row = int(gy)

        if 0 <= col <= (DIMENSION - 1) and 0 <= row <= (DIMENSION - 1):

            tile_x = self.INITIAL_OFFSET_X + (self.HALF_WIDTH * col) - self.HALF_WIDTH * row
            tile_y = self.INITIAL_OFFSET_Y + (self.HALF_HEIGHT * col) + self.HALF_HEIGHT * row
            image = self.local_imgs['grass_block']
            rect = image.get_rect(topleft=(tile_x, tile_y))  # create a rectangle from the top left coord of the image (treat as x,y)
            mask = pygame.mask.from_threshold(image, (0, 0, 0), (1, 1, 1, 255))
            mask.invert()
            if not rect.collidepoint(x, y):  # check if clicked inside where the rect is (in realspace)
                print("nope")
                return False
            check_x, check_y = (x - rect.x, y - rect.y)  # recenter around top_L 0,0
            print(check_x, check_y)
            # print(check_x, check_y)

            if self.camera_rotation_offset == 1:
                col, row = row, DIMENSION - 1 - col
            elif self.camera_rotation_offset == 2:
                col = DIMENSION - 1 - col
                row = DIMENSION - 1 - row
            elif self.camera_rotation_offset == 3:
                col, row = DIMENSION - 1 - row, col

            return col, row, mask.get_at((round(check_x), round(check_y)))  # check if the click is within the boundaries of the image
            #return col, row

        else:
            return None






