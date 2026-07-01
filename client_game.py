import pygame
import json

from client_board_renderer import BoardRenderer
from client_board_state import CharacterSelectedState, CharacterMoveState, CharacterAttackState
from client_ui import HUD
from client_player import PlayerCamera, Player

# IMPORTANT GAME TRACKING OBJECTS
from client_dummy_board import DummyBoard
from client_board_state import BoardIdleState
from client_dummy_shop import DummyShop

# Need to create Shop state object ^

class Game:

    def __init__(self, window, config, ui_manager, client, message_list, num_of_players):
        self.window = window
        self.config = config

        self.player_id = None
        self.message_counter = 0
        self.waiting_for_response_id = None
        self.waiting_for_response = False
        self.client = client
        self.message_list = message_list
        self.new_msg = None

        self.player_turn = 1
        self.player = None
        self.ui_manager = ui_manager

        self.hud = HUD(self)
        #self.shop = DummyShop()
        self.board = DummyBoard()
        self.camera = PlayerCamera(self.config)
        self.board_renderer = BoardRenderer(self)
        self.game_state = BoardIdleState(self)
        self.board_open = True
        self._init()

    def _init(self):
        self.table = {
            "hello": self.say_hello,
            "message": self.print_message,
            "player_id": self.assign_id,
            "CHANGE_TURN": self.change_turn,
            "add_object": self.add_object,
            "MOVE": self.move_character_from_server
        }

    #################
    # Change states #
    #################

    def change_state(self, new_state):
        if hasattr(self.game_state, 'cleanup'):
            self.game_state.cleanup()
        self.game_state = new_state
        print(f"state changed to {new_state}")

    #def open_shop(self):
    #    self.game_state = Shop(self)
    #    print(f"state changed to shop")

    def open_board(self):
        if hasattr(self.game_state, 'cleanup'):
            self.game_state.cleanup()
        self.game_state = BoardIdleState(self)
        print(f"state changed to board")

    def open_character(self, character):
        self.game_state = CharacterSelectedState(self, character)
        print(f"state changed to character selected")

    def draw_screen(self):
        self.game_state.draw()
        if self.waiting_for_response:
            pass
            #print("Waiting for response!!!")
        #self.hud.draw_hud()

    #################
    # Handle clicks #
    #################

    def check_pos(self, x, y):
        #if not self.hud.check_click(x, y):  # i.e. we didn't click a button currently on the screen
        if hasattr(self.game_state, 'handle_click'):
            if not self.waiting_for_response_id:
                self.game_state.handle_click(x, y)
            else:
                print("can't process clicks while waiting for server")

    def check_key_pressed(self, key_press):
        self.game_state.handle_key_pressed(key_press)

    def check_buttons_pressed(self, event):
        if not self.hud.handle_button_pressed(event):
            self.game_state.handle_button_pressed(event)

    ################
    # Handle sever #
    ################

    def process_queue(self):
        while not self.message_list.empty():
            msg = self.message_list.get()
            print(f"message from queue: {msg}")
            self.process_command(msg)

    def process_command(self, msg):
        action_type = msg.get("action")
        message_id = msg.get("message_id")

        function = self.table.get(action_type)

        if function:
            self.new_msg = msg
            function()

            if message_id == self.waiting_for_response_id:
                self.waiting_for_response_id = None
                self.waiting_for_response = False
        else:
            print(f"Unknown command received: {action_type}")

    def assign_id(self):
        self.player_id = self.new_msg.get("id")
        self.player = Player(self.player_id)
        pygame.display.set_caption(f"TURF WARS - player {self.player_id}")

    def move_character_from_server(self):
        col, row = self.new_msg.get("new_col"), self.new_msg.get("new_row")
        character_id = self.new_msg.get("character_id")
        self.board.move_character(character_id, col, row)

    def request_add_object(self):
        msg = json.dumps({"action": "add_object",
                          "col": "3", "row": "3", "object_type": "CHARACTER",
                          "id": f"{self.player_id}"}).encode()
        self.client.client.send(msg)

    def add_object(self):
        row = self.new_msg.get("row")
        col = self.new_msg.get("col")
        object_type = self.new_msg.get("object_type")
        player_id = self.new_msg.get("id")
        self.board.add_object(col, row, object_type, player_id)

    def send_to_server(self, data_dict, message_id):
        try:
            json_string = json.dumps(data_dict).encode('utf-8')
            self.client.client.send(json_string)
            self.waiting_for_response = True
            self.waiting_for_response_id = message_id
            self.message_counter += 1

        except Exception as e:
            print(f"Network error {e}")

    def say_hello(self):
        name = self.new_msg.get("name")
        print(f"Hello {name}!")

    def print_message(self):
        message = self.new_msg.get("text")
        print(f"message from server: {message}")

    def change_turn(self):
        self.player_turn = self.new_msg.get("turn")
        print(f"Now player {self.player_turn}'s turn!")

    def update(self):
        self.process_queue()





