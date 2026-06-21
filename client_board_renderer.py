from constants import *
from layout import *

class BoardRenderer:
    def __init__(self, window, config, camera, images, masks):
        self.window = window
        self.config = config
        self.camera = camera
        self.images = images
        self.masks = masks

        self.HALF_WIDTH = self.config.HALF_WIDTH
        self.HALF_HEIGHT = self.config.HALF_HEIGHT
        self.INITIAL_OFFSET_X = self.config.INITIAL_OFFSET_X
        self.INITIAL_OFFSET_Y = self.config.INITIAL_OFFSET_Y

    def convert_to_tile_coords(self, col, row):
        x = (self.camera.OFFSET_X + (self.HALF_WIDTH * col) - (self.HALF_WIDTH * row))
        y = (self.camera.OFFSET_Y + (self.HALF_HEIGHT * col) + (self.HALF_HEIGHT * row))
        x += self.HALF_WIDTH # create center coords of tile
        y += self.HALF_HEIGHT
        return x, y

    def building_coords(self, x, y, img_key):
        img = self.images[img_key]
        w, h = img.get_size()
        x_build = x - (w/2) + self.HALF_WIDTH * self.camera.zoom_level
        y_build = y - (h/2) + self.HALF_HEIGHT * self.camera.zoom_level
        return x_build, y_build

    def character_coords(self, x, y, img_key):
        img = self.images[img_key]
        w, h = img.get_size()
        x_char = x - (w / 2) + self.HALF_WIDTH * self.camera.zoom_level
        y_char = y - (h / 2) + self.HALF_HEIGHT * self.camera.zoom_level
        return x_char, y_char

    def draw_board(self, dummy_board):
        for column in range(len(dummy_board.tiles)):
            for row in range(len(dummy_board.tiles[column])):
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

                tile = dummy_board.tiles[column_rot][row_rot]
                tile_x, tile_y = self.camera.game_to_camera(tile.x, tile.y) # convert to screen
                img = self.images[tile.img_key]
                self.window.blit(img, (tile_x, tile_y))

                if tile.building:
                    #building = tile.building
                    build_x, build_y = self.building_coords(tile_x, tile_y, 'apartment')
                    self.window.blit(self.images[tile.building.img_key], (build_x, build_y))

                if tile.characters:
                    for character in tile.characters:
                        draw_x, draw_y = self.character_coords(tile_x, tile_y, character.img_key)
                        self.window.blit(self.images[character.img_key], (draw_x, draw_y))

    def check_mask(self, click_x, click_y, img_x, img_y, img_type):

        mask = self.masks[img_type]
        image = self.images[img_type]
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

    def check_click(self, screen_x, screen_y, dummy_board):

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
        #print(f"TEST: target_col: {target_col} target_row: {target_row}")
        tile = dummy_board.tiles[target_col][target_row]

        # Check where tile is on the screen
        tile_x, tile_y = self.convert_to_tile_coords(target_col, target_row)
        tile_screen_x, tile_screen_y = self.camera.game_to_camera(tile_x, tile_y)

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


