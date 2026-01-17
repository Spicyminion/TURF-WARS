from constants import BLOCK_SCALE, DIMENSION
import pygame
import os

class LoadImg:
    def __init__(self, scale_factor):
        self.scale_factor = scale_factor
        self.imgs = {}
        self.path = os.getcwd()
        self.load_imgs()
    '''
    def load_imgs(self):
        for file in os.listdir(self.path):
            if file.lower().endswith(".png") and "block" in file:
                name = os.path.splitext(file)[0] # remove file type
                img = pygame.image.load(file)
                w, h = img.get_size()
                img = pygame.transform.scale(img, (int(w * self.scale_factor * BLOCK_SCALE), int(h * self.scale_factor * BLOCK_SCALE)))
                self.imgs[name] = img
            elif file.lower().endswith(".png"):
                name = os.path.splitext(file)[0]
                img = pygame.image.load(file)
                w, h = img.get_size()
                img = pygame.transform.scale(img, (int(w * self.scale_factor), int(h * self.scale_factor)))
                self.imgs[name] = img
    '''

    def load_imgs(self):
        asset_folders = ['tile_imgs',
        for dir in os.listdir(self.path):
            if file.lower().endswith(".png") and "block" in file:
                name = os.path.splitext(file)[0] # remove file type
                img = pygame.image.load(file)
                w, h = img.get_size()
                img = pygame.transform.scale(img, (int(w * self.scale_factor * BLOCK_SCALE), int(h * self.scale_factor * BLOCK_SCALE)))
                self.imgs[name] = img
            elif file.lower().endswith(".png"):
                name = os.path.splitext(file)[0]
                img = pygame.image.load(file)
                w, h = img.get_size()
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

        self.HALF_WIDTH = self.scale * 25 * BLOCK_SCALE
        self.HALF_HEIGHT = self.scale * 12 * BLOCK_SCALE
        self.INITIAL_OFFSET_X = (self.screen_width / 2) - self.HALF_WIDTH
        self.INITIAL_OFFSET_Y = (self.screen_height / 2) - (self.HALF_HEIGHT * 2 * DIMENSION / 2) # first div brings to mid, 2nd moves up height of half of board

        self.assets = LoadImg(self.scale)
