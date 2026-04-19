import pygame
from layout import layout, TileType, BuildType
from client_tile import Tile, Building
from client_character import Character
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
        self.buttons = []
        self.characters = [Character(10, 10, "smile", 0, 0)]
        self.define_grid()
        self.id = None
        self.player_turn = 1
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
        #self.update_imgs()

    def define_grid(self):
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
                if column == 1 and row == 1:
                    tile = self.tiles[column][row]
                    tile.building = Building(column, row, self.config, BuildType.APARTMENT, 1, x, y, self.HALF_WIDTH, self.HALF_HEIGHT)

    def building_coords(self, x, y, img):
        w, h = img.get_size()
        x_build = x - (w/2) + self.HALF_WIDTH * self.camera.zoom_level
        y_build = y - (h/2) + self.HALF_HEIGHT * self.camera.zoom_level
        return x_build, y_build

    def character_coords(self, x, y, img):
        w, h = img.get_size()
        x_build = x - (w / 2) + self.HALF_WIDTH * self.camera.zoom_level
        y_build = y - (h / 2) + self.HALF_HEIGHT * self.camera.zoom_level
        return x_build, y_build

    def add_object(self, col, row):
        tile = self.tiles[int(col)][int(row)]
        x, y = tile.x, tile.y
        tile.building = Building(col, row, self.config, BuildType.APARTMENT, 1, x, y, self.HALF_WIDTH, self.HALF_HEIGHT)

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
                tile_x, tile_y = self.camera.game_to_camera(tile.x, tile.y)
                img = self.local_imgs[tile.img_key]
                self.window.blit(img, (tile_x, tile_y))
                if tile.building:
                    #building = tile.building
                    build_x, build_y = self.building_coords(tile_x, tile_y, self.local_imgs['apartment'])
                    self.window.blit(self.local_imgs['apartment'], (build_x, build_y))

        for character in self.characters:
            tile = self.tiles[character.row][character.col]
            tile_x, tile_y = self.camera.game_to_camera(tile.x, tile.y)
            draw_x, draw_y = self.character_coords(tile_x, tile_y, self.local_imgs[character.img_key])
            img = self.local_imgs[character.img_key]
            self.window.blit(img, (draw_x, draw_y))


    def game_to_tile(self, x, y):
        pass

    # DEFUNCT MASK AND CLICK CHECKS
    """"
    def check_mask(self, click_x, click_y, img_x, img_y, img_type):
        print(f"click_x {click_x} click_y {click_y}")
        print(f"img_x {img_x} img_y {img_y}")
        mask = self.img_masks[img_type]  # mask is inside a rect starting from 0,0 top left
        image = self.config.assets.imgs[img_type]  # every tile will have the same mask
        rect = image.get_rect(
            topleft=(img_x, img_y))  # create a rectangle from the top left coord of the image (treat as x,y)
        if not rect.collidepoint(click_x, click_y):  # check if clicked inside where the rect is (in realspace)
            # print("not in rect")
            return False
        elif click_x - img_x < 0 or click_y - img_y < 0:
            # print("negative")
            return False
        else:
            check_x, check_y = (click_x - img_x, click_y - img_y)  # recenter around top_L 0,0
            print(f"check_x, check_y {check_x, check_y}")
            return mask.get_at(
                (round(check_x), round(check_y)))  # check if the click is within the boundaries of the image

    
    def check_click(self, screen_x, screen_y):

        # Undo all camera transforms -> game space
        gx, gy = self.camera.camera_to_game(screen_x, screen_y)

        # Translate into tile-local coordinates (0,0 = top-left of top-left tile)
        cx = gx - self.config.INITIAL_OFFSET_X - self.config.HALF_WIDTH
        cy = gy - self.config.INITIAL_OFFSET_Y

        # Normalize by tile dimensions (tile width/height)
        nx = cx / self.HALF_WIDTH
        ny = cy / self.HALF_HEIGHT

        # Convert to isometric tile indices
        col = int((nx + ny) / 2)
        row = int((ny - nx) / 2)

        # Check bounds
        if not (0 <= col < DIMENSION and 0 <= row < DIMENSION):
            return None

        # Correct indices for rotation
        rot = self.camera.rotation_offset % 4
        tile = self.tiles[col][row]
        print(col, row)

        # Check mask
        tile_x = tile.x - self.HALF_WIDTH  # tile.x,y are the center coord of the tile
        tile_y = tile.y - self.HALF_HEIGHT
        print(f"tile_x: {tile_x} tile_y: {tile_y}")
        check = self.check_mask(gx, gy, tile_x, tile_y, 'grass_block')

        if check:
            print(col, row, check)
            if tile.building:
                print("### CHECKING BUILDING ###")
                building = tile.building
                build_x = tile.x - (building.w/2)
                build_y = tile.y - (building.h/2)
                check = self.check_mask(gx, gy, build_x, build_y, 'apartment')
                if check:
                    print("building clicked!")
        else:
            print(col, row, check)
            return None
    """

    def check_mask(self, click_x, click_y, img_x, img_y, img_type):

        mask = self.img_masks[img_type]
        image = self.local_imgs[img_type]

        rect = image.get_rect(topleft=(img_x, img_y))
        if not rect.collidepoint(click_x, click_y):
            return False
        elif click_x - img_x < 0 or click_y - img_y < 0:
            return False
        else:
            check_x, check_y = (click_x - img_x, click_y - img_y)
            return mask.get_at((round(check_x), round(check_y)))

    def check_click(self, screen_x, screen_y, turn):
        rotation = self.camera.rotation_offset
        # Loop in REVERSE draw order (front-to-back visually).
        # This ensures if a building overlaps a tile behind it, you click the building.

        # NEED TO ACCOUNT FOR ROTATION FOR CHARACTERS (NOT IMPLEMENTED)
        # NEED TO STREAMLINE CONVERTING COORDINATES

        for character in self.characters:
            tile = self.tiles[character.row][character.col]
            tile_screen_x, tile_screen_y = self.camera.game_to_camera(tile.x, tile.y)
            img = self.local_imgs[character.img_key]
            char_x, char_y = self.character_coords(tile_screen_x, tile_screen_y, img)
            if self.check_mask(screen_x, screen_y, char_x, char_y, character.img_key):
                print("character clicked!")
                return character

        for column in reversed(range(len(layout))):
            for row in reversed(range(len(layout[column]))):

                # Apply your existing visual rotation swap
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

                # Check where tile is on the screen
                tile_screen_x, tile_screen_y = self.camera.game_to_camera(tile.x, tile.y)

                # Check the building first
                if tile.building:
                    print(f"BUILDING ID: {tile.building.id} PLAYER TURN: {self.player_turn}")
                    if int(tile.building.id) == int(self.player_turn):
                        build_screen_x, build_screen_y = self.building_coords(
                            tile_screen_x, tile_screen_y, self.local_imgs['apartment']
                        )
                        if self.check_mask(screen_x, screen_y, build_screen_x, build_screen_y, 'apartment'):
                            print(f"Building clicked on logical tile: {column_rot}, {row_rot}")
                            return tile.building
                    else:
                        print("not your turn to interact with object")

                # Then check the ground tile mask
                if self.check_mask(screen_x, screen_y, tile_screen_x, tile_screen_y, tile.img_key):
                    print(f"Tile clicked logically at: {column_rot}, {row_rot}")
                    return tile

        return None

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



