import pygame
import json
from client_shop import Shop
from client_board import Board
from client_character import Character, CharacterSelectedState
from client_tile import Tile, Building
from client_ui import HUD, Button
from client_player import PlayerCamera, Player

# IMPORTANT GAME TRACKING OBJECTS
from client_dummy_board import DummyBoard
from client_board_state import BoardIdleState
from client_dummy_shop import DummyShop

# Need to create Shop state object ^

class Game:

    def __init__(self, window, config, client, message_list, NUM_OF_PLAYERS):
        self.window = window
        self.config = config
        self.player_id = None
        self.player_turn = 1
        self.player = None
        self.client = client
        self.message_list = message_list
        self.new_msg = None
        self.UI = HUD(self)
        #self.shop = DummyShop()
        self.board = DummyBoard()
        self.game_state = BoardIdleState(self)  # THIS IS VERY IMPORTANT
        self._init()


    def _init(self):
        self.camera = PlayerCamera(self.config)
        self.table = {
            "hello": self.say_hello,
            "message": self.print_message,
            "player_id": self.assign_id,
            "update_turn": self.update_turn,
            "add_object": self.add_object
        }

    def change_state(self, new_state):
        self.game_state = new_state
        print(f"state changed to {new_state}")

    #def open_shop(self):
    #    self.game_state = Shop(self)
    #    print(f"state changed to shop")

    def open_board(self):
        self.game_state = BoardIdleState(self)
        print(f"state changed to board")

    def open_character(self, character):
        self.game_state = CharacterSelectedState(self, character)
        print(f"state changed to character selected")

    def check_key_pressed(self, key_press):
        if self.state == "BOARD":
            if key_press == pygame.K_z:
                self.zoom(1)
                print("zooming in")
            elif key_press == pygame.K_x:
                self.zoom(-1)
                print("zooming out")
            elif key_press == pygame.K_t:
                print("requesting to change turn ")
                self.change_turn()
            elif key_press == pygame.K_a:
                print("requesting to add object")
                self.request_add_object()
            elif key_press == pygame.K_r:
                self.rotate(1)
            elif key_press == pygame.K_c:
                self.center_board()

    def process_queue(self):
        while not self.message_list.empty():
            msg = self.message_list.get()
            print(f"message from queue: {msg}")
            self.process_command(msg)

    def process_command(self, msg):
        action_type = msg.get("action")
        function = self.table.get(action_type)
        if function:
            self.new_msg = msg
            function()
        else:
            print("Unknown command received")

    def assign_id(self):
        self.player_id = self.new_msg.get("id")
        self.player = Player(self.player_id)
        self.board.player_id = self.player_id

    def update_turn(self):
        msg = self.new_msg.get("turn")
        self.player_turn = msg
        self.board.player_turn = self.player_turn

    def request_add_object(self):
        msg = json.dumps({"action": "add_object",
                          "col": "3", "row": "3", "object_type": "CHARACTER",
                          "id": f"{self.player_id}"}).encode()
        self.client.client.send(msg)

    def cancel_action(self):
        self.action_state = "NONE"
        self.state = "BOARD"
        self.UI.state = "BOARD"
        self.selected_char = None

    def add_object(self):
        row = self.new_msg.get("row")
        col = self.new_msg.get("col")
        object_type = self.new_msg.get("object_type")
        player_id = self.new_msg.get("id")
        self.board.add_object(col, row, object_type, player_id)

    def say_hello(self):
        name = self.new_msg.get("name")
        print(f"Hello {name}!")

    def print_message(self):
        message = self.new_msg.get("text")
        print(f"message from server: {message}")

    def change_turn(self):
        print(f"player_id: {self.player_id} player turn: {self.player_turn}")
        if int(self.player_id) == int(self.player_turn):
            msg = {"action": "change_turn", "id": f"{self.player_id}"}
            self.client.client.send(json.dumps(msg).encode())

    def check_pos(self, x, y):
        if not self.UI.check_click(x, y, self.state):  # i.e. we didn't click a button currently on the screen
            self.click_table[self.state](x, y, self.player_turn) # ignore syntax warning (pass click accordingly)
        print(f"game state: {self.state} action state: {self.action_state}")

    def handle_board(self, x, y, turn):
        obj = self.board.check_click(x, y, turn)
        print(f"object clicked is: {obj}")
        if self.state == "CHARACTER_SELECTED":
            if self.action_state != "NONE":
                if obj is None:
                    self.action_state = "NONE"
                    self.state = "BOARD"
                    self.UI.state = "BOARD"
                    print("exiting character selection without making an action")
                    return
                self.action_table[self.action_state](obj)
                self.action_state = "NONE"
                self.selected_char = None
                self.set_state("BOARD")
        elif self.state == "BOARD":
            if isinstance(obj, Character):
                self.set_state("CHARACTER_SELECTED")
                self.selected_char = obj
            else:
                self.set_state("BOARD")


    def zoom(self, zoom):
        check = self.camera.zoom_level + zoom
        if check < 1 or check > 3:
            pass
        else:
            self.camera.zoom_level+=zoom
            self.camera.move_camera()
            self.board.update_imgs()
            self.board.update_masks()
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

    def center_board(self):
        self.camera.center_board()
        self.board.update_imgs()
        self.board.update_masks()
        self.board.draw_board()

    def update(self):
        self.process_queue()
        self.draw_table[self.state]()
        self.UI.draw()

class GameState:
    def __init__(self, game):
        self.game = game



