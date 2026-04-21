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
        self.buildings = []
        self.characters = []
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
                self.tiles[column].append(Tile(tile_type, column, row, x + self.HALF_WIDTH, y + self.HALF_HEIGHT)) # true center
                if column == 1 and row == 1:
                    tile = self.tiles[column][row]
                    tile.building = Building(column, row, self.config, BuildType.APARTMENT, 1)
        self.add_object(3, 3, "CHARACTER", 1)

    def building_coords(self, x, y, img_key):
        img = self.local_imgs[img_key]
        w, h = img.get_size()
        x_build = x - (w/2) + self.HALF_WIDTH * self.camera.zoom_level
        y_build = y - (h/2) + self.HALF_HEIGHT * self.camera.zoom_level
        return x_build, y_build

    def character_coords(self, x, y, img_key):
        img = self.local_imgs[img_key]
        w, h = img.get_size()
        x_char = x - (w / 2) + self.HALF_WIDTH * self.camera.zoom_level
        y_char = y - (h / 2) + self.HALF_HEIGHT * self.camera.zoom_level
        return x_char, y_char

    def add_object(self, col, row, object_type, player_id):
        tile = self.tiles[int(col)][int(row)]
        x, y = tile.x, tile.y
        if object_type == "CHARACTER":
            char = Character(10, 10, "smile", col, row, player_id)
            tile.characters.append(char)
            self.characters.append(char)
        elif object_type == "BUILDING":
            build = Building(col, row, self.config, BuildType.APARTMENT, player_id)
            tile.building = Building(col, row, self.config, BuildType.APARTMENT, player_id)
            self.buildings.append(build)

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
                tile_x, tile_y = self.camera.game_to_camera(tile.x, tile.y) # convert to screen
                img = self.local_imgs[tile.img_key]
                self.window.blit(img, (tile_x, tile_y))

                if tile.building:
                    #building = tile.building
                    build_x, build_y = self.building_coords(tile_x, tile_y, 'apartment')
                    self.window.blit(self.local_imgs['apartment'], (build_x, build_y))

                if tile.characters:
                    for character in tile.characters:
                        draw_x, draw_y = self.character_coords(tile_x, tile_y, character.img_key)
                        self.window.blit(self.local_imgs[character.img_key], (draw_x, draw_y))

    def check_mask(self, click_x, click_y, img_x, img_y, img_type):

        mask = self.img_masks[img_type]
        image = self.local_imgs[img_type]
        rect = image.get_rect(topleft=(img_x, img_y))

        if not rect.collidepoint(click_x, click_y):
            return False
        else:
            check_x = click_x - img_x
            check_y = click_y - img_y
            if mask.get_at((int(check_x), int(check_y))):
                return True
            else:
                return False

    def check_click(self, screen_x, screen_y, turn):

        gx, gy = self.camera.camera_to_game(screen_x, screen_y)
        cx = gx - self.INITIAL_OFFSET_X - self.HALF_WIDTH
        cy = gy - self.INITIAL_OFFSET_Y

        # Normalize by tile dimensions
        nx = cx / self.HALF_WIDTH
        ny = cy / self.HALF_HEIGHT

        # Convert to approximate logical indices
        target_col = int((nx + ny) / 2)
        target_row = int((ny - nx) / 2)

        if target_col < 0 or target_col >= DIMENSION or target_row < 0 or target_row >= DIMENSION:
            print("Clicked outside the board bounds!")
            return None

        # Print the tile clicked on
        print(f"TEST: target_col: {target_col} target_row: {target_row}")
        tile = self.tiles[target_col][target_row]

        # Check where tile is on the screen

        tile_screen_x, tile_screen_y = self.camera.game_to_camera(tile.x, tile.y)
        if tile.characters:
            for character in tile.characters:
                char_x, char_y = self.character_coords(tile_screen_x, tile_screen_y, character.img_key)
                if self.check_mask(screen_x, screen_y, char_x, char_y, character.img_key):
                    print(f"CHARACTER clicked on tile: {target_col}, {target_row}")
                    return character
        if tile.building:
            build_screen_x, build_screen_y = self.building_coords(
                tile_screen_x, tile_screen_y, 'apartment')
            if self.check_mask(screen_x, screen_y, build_screen_x, build_screen_y, 'apartment'):
                print(f"BUILDING clicked on tile: {target_col}, {target_row}")
                return tile.building
        if self.check_mask(screen_x, screen_y, tile_screen_x, tile_screen_y, tile.img_key):
            print(f"Tile: {target_col}, {target_row} clicked")
            return tile
        else:
            return None
