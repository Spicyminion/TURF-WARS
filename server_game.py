import pygame
from client_board import Board, UI
from client_player import PlayerCamera
class Game:

    def __init__(self, window, config, NUM_OF_PLAYERS):

        self.players = []
        self.player_turn = 1
        self._init()

    def _init(self):
        self.board = Board()
        #self.ui.buttons.append(Button(10, 10, self.change_turn()))
        #self.ui.draw_buttons(self.window)

    def change_turn(self):
        if self.player_turn == len(self.players):
            self.player_turn = 1
        else:
            self.player_turn += 1

    def update(self):
        self.board.draw_board()
'''
class MoveCommand():
    def __init__(self):
'''