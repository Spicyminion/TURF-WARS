import pygame
from server_board import Board
from client_player import PlayerCamera
class Game:

    def __init__(self):

        self.clients = []
        self.players = [0]
        self.player_turn = 1
        self.table = {
            "change_turn": self.change_turn
        }
        self.msg = None
        self._init()

    def _init(self):
        self.board = Board()

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