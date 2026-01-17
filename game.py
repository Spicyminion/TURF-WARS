import pygame
from board import Board
class Game:

    def __init__(self, window, config):
        self.window = window
        self.config = config
        self._init()

    def _init(self):
        self.board = Board(self.window, self.config)
        self.board.draw_board(self.window)

    def update(self):
        self.board.draw_board(self.window)

    def get_space(self, row, col, x, y):
        print(self.board.tiles[row][col].check_click(x, y))

