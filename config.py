from constants import BLOCK_SCALE, DIMENSION
import pygame
import os

class LoadImg:
    def __init__(self, scale_factor):
        self.scale_factor = scale_factor
        self.imgs = {}
        self.path = os.getcwd()
        self.load_imgs()

    def load_imgs(self):
        for directory in os.listdir(self.path):
            dir_path = os.path.join(self.path, directory)
            if dir_path and dir_path.endswith("_imgs"):
                for png in os.listdir(dir_path):
                    name = os.path.splitext(png)[0] # remove file type
                    img = pygame.image.load(os.path.join(dir_path, png)).convert()
                    img.set_colorkey((0, 0, 0))
                    w, h = img.get_size()
                    if png.lower().endswith(".png") and "block" in png:
                        img = pygame.transform.scale(img, (int(w * self.scale_factor * BLOCK_SCALE), int(h * self.scale_factor * BLOCK_SCALE)))
                    else:
                        img = pygame.transform.scale(img, (int(w * self.scale_factor), int(h * self.scale_factor)))
                    self.imgs[name] = img


    def get(self, name):
        return self.imgs[name]

class ConfigGame:
    def __init__(self, screen_width, screen_height):
        self.screen_width = int(screen_width * 0.9)
        self.screen_height = int(screen_height * 0.9)

        self.scale = min(
            self.screen_width / 1800,  # 1800, 900 are internal resolution
            self.screen_height / 900
        )

        self.HALF_WIDTH = self.scale * 25 * BLOCK_SCALE  # DEFAULT TILE DIMENSIONS
        self.HALF_HEIGHT = self.scale * 12 * BLOCK_SCALE
        self.INITIAL_OFFSET_X = (self.screen_width / 2) - self.HALF_WIDTH # subtract to center tile
        self.INITIAL_OFFSET_Y = (self.screen_height / 2) - (self.HALF_HEIGHT * 2 * DIMENSION / 2) # first div brings to mid, 2nd moves up height of half of board

    def load_imgs(self):
        self.assets = LoadImg(self.scale)



