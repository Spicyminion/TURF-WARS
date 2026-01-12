import pygame
from board import Board
class Game:

    def __init__(self, window):
        self.window = window
        self._init()

    def _init(self):
        self.board = Board(self.window)
        self.board.draw_board(self.window)

    def update(self):
        self.board.draw_board(self.window)