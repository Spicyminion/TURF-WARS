import pygame
from board import Board, UI
from tile import Button
class Game:

    def __init__(self, window, config):
        self.window = window
        self.config = config
        self._init()

    def _init(self):
        self.board = Board(self.window, self.config)
        self.ui = UI()
        self.board.draw_board(self.window)
        self.ui.buttons.append(Button(10, 10, 'apartment', self.config))

    def update(self):
        self.board.draw_board(self.window)
        self.ui.draw_buttons(self.window)

    def get_space(self, row, col, x, y):
        print(self.board.tiles[row][col].check_click(x, y))

    def get_button(self, x, y):
        print(self.ui.check_buttons(x, y))
