import pygame
from layout import layout, TileType
from tile import Tile, Building, Button
from constants import DIMENSION

#class BoardState()


class Board:

    def __init__(self, window, config, camera):
        self.window = window
        self.config = config
        self.local_imgs = {}
        self.img_masks = {}
        self.INITIAL_OFFSET_X = self.config.INITIAL_OFFSET_X
        self.INITIAL_OFFSET_Y = self.config.INITIAL_OFFSET_Y
        self.HALF_HEIGHT = self.config.HALF_HEIGHT
        self.HALF_WIDTH = self.config.HALF_WIDTH
        self.camera = camera
        self.board_center = (self.config.screen_width / 2) + (self.config.screen_height / 2) # start at true center of board
        self.tiles = []
        self.define_grid()
        for name,img in self.config.assets.imgs.items():
            self.local_imgs[name] = img
        self.update_masks()

    def update_imgs(self):
        zoom = self.camera.zoom_level
        for name, img in self.config.assets.imgs.items():
            w, h = img.get_size()
            img = pygame.transform.scale(img, (round(w * zoom), round(h * zoom)))
            self.local_imgs[name] = img
        #self.draw_board()

    def update_masks(self):
        for name, img in self.local_imgs.items():
            mask = pygame.mask.from_threshold(img, (0, 0, 0), (1, 1, 1, 255))
            mask.invert()
            self.img_masks[name] = mask

    def define_grid(self):
        id = 0
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                self.tiles[column].append(Tile(tile_type, column, row))
                id += 1
                if column == 1 and row == 1:
                    tile = self.tiles[column][row]
                    tile.building = Building(column, row, self.config)

    def draw_board(self):
        for column in range(len(layout)):
            for row in range(len(layout[column])):
                rotation = self.camera.rotation_offset
                if rotation == 1:
                    column_rot = row
                    row_rot = DIMENSION - 1 - column
                elif rotation == 2:
                    column_rot = DIMENSION - 1 - column
                    row_rot = DIMENSION - 1 - row
                elif rotation == 3:
                    column_rot = DIMENSION - 1 - row
                    row_rot = column
                else:
                    column_rot = column
                    row_rot = row

                tile = self.tiles[column_rot][row_rot]
                img = self.local_imgs[tile.img_key]

                x = (
                        self.camera.OFFSET_X
                        + (self.HALF_WIDTH * column * self.camera.zoom_level)
                        - (self.HALF_WIDTH * row * self.camera.zoom_level)
                )
                y = (
                        self.camera.OFFSET_Y +
                        (self.HALF_HEIGHT * column * self.camera.zoom_level) +
                        (self.HALF_HEIGHT * row * self.camera.zoom_level)
                )

                self.window.blit(img, (x, y))
                if column_rot == 1 and row_rot == 1:
                    #print(tile.building)
                    tile.building.draw_building(self.window, self.HALF_HEIGHT, self.HALF_WIDTH, x, y)

    def check_mask(self, click_x, click_y, img_x, img_y, img_type):
        mask = self.img_masks[img_type]  # mask is inside a rect starting from 0,0 top left
        image = self.local_imgs[img_type]  # every tile will have the same mask
        rect = image.get_rect(
            topleft=(img_x, img_y))  # create a rectangle from the top left coord of the image (treat as x,y)
        if not rect.collidepoint(click_x, click_y):  # check if clicked inside where the rect is (in realspace)
            print("nope")
            return False
        else:
            check_x, check_y = (click_x - img_x, click_y - img_y)  # recenter around top_L 0,0
            return mask.get_at((round(check_x), round(check_y))) # check if the click is within the boundaries of the image

    def check_click(self, x, y):

        # Recenter to remove any visual adjustments (zoom, rotation, camera movement)

        cx, cy = x - self.camera.OFFSET_X - self.HALF_WIDTH, y - self.camera.OFFSET_Y  # (0, 0) is top L of top tile
        # print(f"x,y:{x, y} cx,cy: {cx, cy}")

        # Now normalize x & y coords to width and height of each tile respectively (units for moving)
        half_width = self.HALF_WIDTH * self.camera.zoom_level
        half_height = self.HALF_HEIGHT * self.camera.zoom_level
        nx = cx / half_width
        ny = cy / half_height

        # Next convert into x, y within range of (6,6) 7x7 tiles (0-based idx)
        gx = (nx + ny) / 2
        gy = (ny - nx) / 2

        # Compute which tile is being used
        col = int(gx)
        row = int(gy)

        if 0 <= col <= (DIMENSION - 1) and 0 <= row <= (DIMENSION - 1):
            tile_x = self.camera.OFFSET_X + (half_width * col) - half_width * row
            tile_y = self.camera.OFFSET_Y + (half_height * col) + half_height * row
            check = self.check_mask(x, y, tile_x, tile_y, 'grass_block')
            if check == 1:
                col_rot, row_rot = col, row
                if self.camera.rotation_offset == 1:
                    col_rot, row_rot = row, DIMENSION - 1 - col
                elif self.camera.rotation_offset == 2:
                    col_rot = DIMENSION - 1 - col
                    row_rot = DIMENSION - 1 - row
                elif self.camera.rotation_offset == 3:
                    col_rot, row_rot = DIMENSION - 1 - row, col
                tile = self.tiles[col_rot][row_rot]
                if tile.building:
                    self.check_mask()
                return col_rot, row_rot, check
            else:
                return None
        else:
            return None



#class Board


class UI:
    def __init__(self):
        self.buttons = []

    def check_buttons(self, x, y):
        for button in self.buttons:
            if button.check_click(x, y):
                break

    def draw_buttons(self, window):
        for button in self.buttons:
            button.draw(window)



