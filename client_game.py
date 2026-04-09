import pygame
import json
from client_board import Board, UI
from client_player import PlayerCamera
from tile import Button
class Game:

    def __init__(self, window, config, client, message_list, NUM_OF_PLAYERS):
        self.window = window
        self.config = config
        self.players = []
        self.player_turn = 1
        self.client = client
        self.message_list = message_list
        self._init()

    def _init(self):
        self.camera = PlayerCamera(self.config)
        self.board = Board(self.window, self.config, self.camera)
        self.ui = UI()
        self.table = {
            "hello": self.say_hello,
            "message": self.print_message
        }

        #self.ui.buttons.append(Button(10, 10, self.change_turn()))
        #self.ui.draw_buttons(self.window)

    def test_send(self):
        self.client.send("HELLO SERVER")

    def process_queue(self):
        while not self.message_list.empty():
            msg = self.message_list.get()
            print(f"message from queue: {msg}")
            self.process_command(msg)

    def process_command(self, new_msg):
        action_type = new_msg.get("action")
        function = self.table.get(action_type)
        if function:
            function(new_msg)
        else:
            print("Unknown command received")

    def say_hello(self, new_msg):
        name = new_msg.get("name")
        print(f"Hello {name}!")

    def print_message(self, new_msg):
        message = new_msg.get("text")
        print(f"message from server: {message}")

    def get_button(self, x, y):
        self.ui.check_buttons(x, y)

    def check_pos(self, x, y, ):
        self.board.check_click(x, y)

    def check_all(self, d1, d2, x, y ):
        for build in self.board.tiles[d1][d2].building:
            if build.check_click(x, y):
                 build.draw_stat(self.window)

    def zoom(self, zoom):
        check = self.camera.zoom_level + zoom
        if check < 1 or check > 3:
            pass
        else:
            self.camera.zoom_level+=zoom
            self.camera.move_camera()
            self.board.update_imgs()
            #self.board.update_masks()
            self.board.draw_board()

    def move_y(self, increment):
        self.camera.y_offset += increment
        self.camera.move_camera()
        self.board.draw_board()

    def move_x(self, increment):
        self.camera.x_offset += increment
        self.camera.move_camera()
        self.board.draw_board()

    def rotate(self, direction):
        check = self.camera.rotation_offset + direction
        if check > 3:
            self.camera.rotation_offset = 0
        elif check < 0:
            self.camera.rotation_offset = 3
        else:
            self.camera.rotation_offset += direction
        self.board.update_imgs()

    def change_turn(self):
        if self.player_turn == len(self.players):
            self.player_turn = 1
        else:
            self.player_turn += 1

    def center_board(self):
        self.camera.center_board()
        self.board.update_masks()
        #self.board.draw_board()

    def draw_board(self):
        self.board.draw_board()

    def update(self):
        self.process_queue()
        self.board.draw_board()
'''
class MoveCommand():
    def __init__(self):
'''