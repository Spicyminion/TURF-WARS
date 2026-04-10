import pygame
from server_board import Board
import json
import queue
class Game:

    def __init__(self, message_list):

        self.clients = []
        self.players = [0]
        self.player_turn = 1
        self.table = {
            "change_turn": self.change_turn
        }
        self.message_list = message_list
        self.new_msg = None
        self._init()

    def _init(self):
        self.board = Board()

    def process_queue(self):
            msg = self.message_list.get() # will stop here until a new message
            print(f"message from queue: {msg}")
            msg = json.loads(msg) # convert to dict
            self.process_command(msg)

    def process_command(self, msg):
        action_type = msg.get("action")
        function = self.table.get(action_type)
        if function:
            self.new_msg = msg
            function()
        else:
            print("Unknown command received")

    def change_turn(self):
        player_id = self.new_msg.get("id")
        if player_id == self.player_turn:
            if self.player_turn == len(self.players):
                self.player_turn = 1
            else:
                self.player_turn += 1
            for client in self.clients:
                turn = {"action": "update_turn", "turn": f"{self.player_turn}"}
                client.send(json.dumps(turn).encode())


    def say_hello(self):
        name = self.new_msg.get("name")
        print(f"Hello {name}!")

    def update(self):
        pass
        # do something for board

'''
class MoveCommand():
    def __init__(self):
'''