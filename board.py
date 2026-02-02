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
        self.update_imgs()

    def define_grid(self):
        id = 0
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                x = (
                        self.camera.OFFSET_X
                        + (self.HALF_WIDTH * column)
                        - (self.HALF_WIDTH * row)
                )
                y = (
                        self.camera.OFFSET_Y +
                        (self.HALF_HEIGHT * column) +
                        (self.HALF_HEIGHT * row)
                )
                #if column == 0 and row == 0:
                #    print(f"ORIG TILE_X{x} ORIG TILE_Y{y}")
                self.tiles[column].append(Tile(tile_type, column, row, x + self.HALF_WIDTH, y + self.HALF_HEIGHT)) # true center
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
                #print(f"board: {tile.x, tile.y}")
                tile_x, tile_y = self.camera.game_to_camera(tile.x, tile.y)
                #if column == 0 and row == 0 and self.camera.rotation_offset == 1:
                #    print(f"ROT: {self.camera.rotation_offset} TILE_X:{tile_x}, TILE_Y:{tile_y}")

                img = self.local_imgs[tile.img_key]
                self.window.blit(img, (tile_x, tile_y))
                if tile.building:
                    pass

    def game_to_tile(self, x, y):
        pass

    def check_mask(self, click_x, click_y, img_x, img_y, img_type):
        mask = self.img_masks[img_type]  # mask is inside a rect starting from 0,0 top left
        image = self.local_imgs[img_type]  # every tile will have the same mask
        rect = image.get_rect(
            topleft=(img_x, img_y))  # create a rectangle from the top left coord of the image (treat as x,y)
        if not rect.collidepoint(click_x, click_y):  # check if clicked inside where the rect is (in realspace)
            print("not in rect")
            return False
        elif click_x - img_x < 0 or click_y - img_y < 0:
            print("negative")
            return False
        else:
            check_x, check_y = (click_x - img_x, click_y - img_y)  # recenter around top_L 0,0
            return mask.get_at((round(check_x), round(check_y))) # check if the click is within the boundaries of the image

    def check_click(self, screen_x, screen_y):
        """
        Check which tile the user clicked on, accounting for:
        - camera zoom
        - camera pan
        - camera rotation
        """

        # 1) Undo all camera transforms → game space
        gx, gy = self.camera.camera_to_game(screen_x, screen_y)

        # 2) Translate into tile-local coordinates (0,0 = top-left of top-left tile)
        cx = gx - self.config.INITIAL_OFFSET_X - self.config.HA
        cy = gy - self.config.INITIAL_OFFSET_Y

        # 3) Normalize by tile dimensions (diamond width/height)
        nx = cx / self.HALF_WIDTH
        ny = cy / self.HALF_HEIGHT

        # 4) Convert to isometric tile indices
        col = int((nx + ny) / 2)
        row = int((ny - nx) / 2)

        # Check bounds
        if not (0 <= col < DIMENSION and 0 <= row < DIMENSION):
            return None

        # 5) Correct indices for rotation
        rot = self.camera.rotation_offset % 4
        if rot == 0:
            col_rot, row_rot = col, row
        elif rot == 1:  # 90°
            col_rot, row_rot = row, DIMENSION - 1 - col
        elif rot == 2:  # 180°
            col_rot, row_rot = DIMENSION - 1 - col, DIMENSION - 1 - row
        elif rot == 3:  # 270°
            col_rot, row_rot = DIMENSION - 1 - row, col

        tile = self.tiles[col_rot][row_rot]

        # 6) Check mask
        tile_x = tile.x - self.HALF_WIDTH  # top-left
        tile_y = tile.y - self.HALF_HEIGHT
        check = self.check_mask(gx, gy, tile_x, tile_y, 'grass_block')

        if check:
            print(col_rot, row_rot, check)
            return col_rot, row_rot, check
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



