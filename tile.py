import pygame
from constants import HALF_HEIGHT, HALF_WIDTH, BLOCK, CLICKED_BLOCK, TileType, INITIAL_OFFSET_Y, INITIAL_OFFSET_X, APARTMENT, COLOR_KEY
#import constants

class Clickable:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y)) # create a rectangle from the top left coord of the image (treat as x,y)
        self.mask = pygame.mask.from_threshold(image, COLOR_KEY, (1,1,1,255))

    def check_click(self, click_x, click_y):
        if not self.rect.collidepoint(click_x, click_y): # check if clicked inside where the rect is (in realspace)
            return False
        check_x, check_y = (click_x - self.rect.x, click_y - self.rect.y)  # recenter around top_L 0,0
        print(check_x, check_y)
        return self.mask.get_at((check_x, check_y))  # check if the click is within the boundaries of the image

    def draw(self, window):
        window.blit(self.image, self.rect.topleft) # print where top left of rectangle is
        pygame.draw.rect(window, (255, 0, 0), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2 )


class Tile(Clickable):
    def __init__(self, type, x, y, col, row):

        if type == TileType.BLANK:
            use_image = BLOCK
        else:
            use_image = CLICKED_BLOCK
        super().__init__(x, y, use_image)

        self.row = row
        self.col = col
        self.type = type
        self.characters = []

    def check_pos(self):
        print(self.rect.x)


'''
class Building(Clickable):
    def __init__(self, x, y):
        self.x = x
        self.y = y
'''