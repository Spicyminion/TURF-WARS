import pygame
from constants import COLOR_KEY
from layout import TileType
#import constants

class Clickable:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y)) # create a rectangle from the top left coord of the image (treat as x,y)
        self.mask = pygame.mask.from_threshold(image, COLOR_KEY, (1,1,1,255))
        self.mask.invert()

    def check_click(self, click_x, click_y):
        if not self.rect.collidepoint(click_x, click_y): # check if clicked inside where the rect is (in realspace)
            return False
        check_x, check_y = (click_x - self.rect.x, click_y - self.rect.y)  # recenter around top_L 0,0
        #print(check_x, check_y)
        return self.mask.get_at((check_x, check_y))  # check if the click is within the boundaries of the image

    def draw(self, window):
        window.blit(self.image, self.rect.topleft) # print where top left of rectangle is
        #pygame.draw.rect(window, (255, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2 )


class Tile(Clickable):
    def __init__(self, type, x, y, col, row, config, id):

        if type == TileType.BLANK:
            use_image = config.assets.get('grass_block')
        else:
            use_image = config.assets.get('clicked_block')
        super().__init__(x, y, use_image)

        self.row = row
        self.col = col
        self.type = type
        self.config = config
        self.id = id
        self.characters = []
        self.building = []

    def check_pos(self):
        print(self.rect.x)

    def draw(self, window):
        super().draw(window)
        for structure in self.building:
            structure.draw(window)

    def check_click(self, click_x, click_y):
        if super().check_click(click_x, click_y):
            check = True
            print("Tile_selected")
            for character in self.characters:
                if character.check_click(click_x, click_y):
                    check = False
                    break
            if check:
                for building in self.building:
                    if building.check_click(click_x, click_y):
                        print("building clicked!")
                        break


class Building(Clickable):
    def __init__(self, x, y, col, row, config):

        img = config.assets.get('apartment')
        w, h = img.get_size()
        x = x - w / 2
        y = y - h / 2
        super().__init__(x, y, img)
        self.config = config
        self.row = row
        self.col = col

    def check_pos(self):
        print(self.rect.x)

    def draw_stat(self, window):
        test = self.config.assets.get('test_stat')
        w, h = self.rect.w, self.rect.h
        x, y = self.rect.x + w/2 - test.get_size()[0] / 2, self.rect.y
        window.blit(test, (x, y))

class Button(Clickable):
    def __init__(self, x, y, image, config):

        use_image = config.assets.get(image)
        super().__init__(x, y, use_image)
        self.config = config

    def check_click(self, click_x, click_y):
        if super().check_click(click_x, click_y):
            print("button clicked!")
