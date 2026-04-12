import pygame
from constants import COLOR_KEY
from layout import TileType, TILETYPE_TO_SPRITE
#import constants

class Tile:
    def __init__(self, type, col, row, x, y):
        self.row = row
        self.col = col
        self.type = type
        self.img_key = TILETYPE_TO_SPRITE[type]
        self.x = x
        self.y = y
        self.characters = []
        self.building = None
        self.id = None

    def check_click(self, click_x, click_y):
        check = True
        for character in self.characters:
            if character.check_click(click_x, click_y):
                check = False
                break
        if check:
            for building in self.building:
                if building.check_click(click_x, click_y):
                    print("building clicked!")
                    break

class Building:
    def __init__(self, col, row, config, type, id,
                 tile_x, tile_y, tile_width, tile_height):
        self.row = row
        self.col = col
        self.config = config
        self.type = type
        self.img = self.config.assets.imgs['apartment']
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.w, self.h = self.img.get_size()
        self.x = tile_x + (self.w/2)  # tile x,y is the center of the tile
        self.y = tile_y + (self.h/2)
        self.draw_x = tile_x + self.tile_width - (self.w / 2)
        self.draw_y = tile_y + self.tile_height - (self.h / 2)
        self.id = id

    def draw_coords(self, x, y):
        draw_x = x - self.w/2
        draw_y = y - self.h/2
        return draw_x, draw_y

    '''
    def draw_stat(self, window, x, y):
        test = self.config.assets.get('test_stat')
        w, h = self.rect.w, self.rect.h
        x, y = self.rect.x + w/2 - test.get_size()[0] / 2, self.rect.y
        window.blit(test, (x, y))
    '''


class Button:
    def __init__(self, x, y, command, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = None
        self.command = command
        self.make_mask()

    def make_mask(self):
        self.mask = pygame.mask.from_threshold(self.img, (0, 0, 0), (1, 1, 1, 255))
        self.mask.invert()

    def check_mask(self, click_x, click_y):
        rect = self.img.get_rect(topleft=(self.x, self.y))
        if not rect.collidepoint(click_x, click_y):
            print("not clicked")
        elif click_x - self.x < 0 or click_y - self.y < 0:
            print("not clicked")
        else:
            check_x, check_y = (click_x - self.x, click_y - self.y)
            if self.mask.get_at((round(check_x), round(check_y))):
                print("BUTTON PRESSED")
                self.command()



    '''
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
    '''

    def get_rect(self):
        return self.x, self.y

    def on_click(self):
        self.command.execute()





