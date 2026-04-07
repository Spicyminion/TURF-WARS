import pygame
from server_board import Board
from client_player import PlayerCamera
class Game:

    def __init__(self):

        self.players = []
        self.player_turn = 1
        self.table = {

        }
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
        # do something for board
        pass

'''
class MoveCommand():
    def __init__(self):
'''