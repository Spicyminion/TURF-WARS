import pygame
from board import Board, UI
from tile import Button
class Game:

    def __init__(self, window, config):
        self.window = window
        self.config = config
        self.players = []
        self._init()

    def _init(self):
        self.board = Board(self.window, self.config)
        self.board.draw_board(self.window)
        self.ui = UI()
        self.ui.buttons.append(Button(10, 10, 'apartment', self.config))
        self.ui.draw_buttons(self.window)

    def update(self):
        self.board.draw_board(self.window)
        self.ui.draw_buttons(self.window)

    def get_space(self, col, row, x, y):
        print(self.board.tiles[col][row].check_click(x, y))

    def get_button(self, x, y):
        self.ui.check_buttons(x, y)

    def check_all(self, d1, d2, x, y ):
        for build in self.board.tiles[d1][d2].building:
            if build.check_click(x, y):
                build.draw_stat(self.window)

    def zoom(self):
        self.zoom = self.zoom * 1.2
        self.config.update_zoom(self.zoom)