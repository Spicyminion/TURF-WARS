import pygame
from client_dummy_board import DummyBoard
import json
import queue
class Game:

    def __init__(self, message_list):

        self.clients = []
        self.players = []
        self.player_turn = 1
        self.message_list = message_list
        self.board = DummyBoard()
        self.new_msg = None
        self.table = {
            "CHANGE_TURN": self.change_turn,
            "add_object": self.add_object,
            "MOVE": self.move_character,
        }
        self.game_state = None

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
        player_id = self.new_msg.get("player_id")
        if int(player_id) == int(self.player_turn):
            if int(self.player_turn) == len(self.clients):
                self.player_turn = 1
            else:
                self.player_turn += 1
            for client in self.clients:
                print("send turn update")
                turn = {"action": "CHANGE_TURN", "turn": f"{self.player_turn}"}
                client.send(json.dumps(turn).encode())

    def move_character(self):
        char_id = self.new_msg.get("character_id")
        new_col = self.new_msg.get("new_col")
        new_row = self.new_msg.get("new_row")

        if self.board.move_character(char_id, new_col, new_row):
            msg = json.dumps(self.new_msg).encode('utf-8')  # reconvert back to json
            for client in self.clients:
                client.send(msg)
                print(f"send move update to {client}")


    def add_object(self):
        print("passing object to clients")
        col = self.new_msg.get("col")
        row = self.new_msg.get("row")
        player_id = self.new_msg.get("id")
        object_type = self.new_msg.get("object_type")
        msg = {"action": "add_object",
               "col": f"{col}", "row": f"{row}", "object_type": f"{object_type}",
               "id": f"{player_id}",}
        self.board.add_objects(msg)
        for client in self.clients:
            client.send(json.dumps(msg).encode())

    def say_hello(self):
        name = self.new_msg.get("name")
        print(f"Hello {name}!")

    def update(self):
        pass
        # do something for board
