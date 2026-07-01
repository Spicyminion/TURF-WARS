import pygame
from base_state import GameState
from client_ui import Button
import pygame_gui
import json
from client_board_renderer import BoardRenderer
from client_character import Character

class BoardViewState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.renderer = game.board_renderer
        self.board = game.board
        self.window = game.window
        self.camera = game.camera
        self.ui_manager = game.ui_manager
        self.player_turn = game.player_turn

    def handle_key_pressed(self, key_press):
        if key_press == pygame.K_z:
            self.renderer.zoom(1)
            print("zooming in")
        elif key_press == pygame.K_x:
            self.renderer.zoom(-1)
            print("zooming out")
        elif key_press == pygame.K_r:
            self.renderer.rotate(1)
        elif key_press == pygame.K_c:
            self.renderer.center_board()

    def handle_continuous_inputs(self, keys):
        if keys[pygame.K_UP]:
            self.renderer.move_y(-5)
        elif keys[pygame.K_DOWN]:
            self.renderer.move_y(5)
        elif keys[pygame.K_LEFT]:
            self.renderer.move_x(-5)
        elif keys[pygame.K_RIGHT]:
            self.renderer.move_x(5)

    def draw(self):
        self.renderer.draw_board(self.board)

class BoardIdleState(BoardViewState):
    def __init__(self, game):
        super().__init__(game)

    def handle_click(self, x, y):
        object_type, clicked_object = self.renderer.check_click(x, y, self.board)  # renderer will handle what is clicked
        print(f"clicked object type: {object_type}")
        if object_type == "CHAR":
            print("CHARACTER CLICKED!!!")
            self.game.open_character(clicked_object)

    def handle_button_pressed(self, event):
        pass

class CharacterSelectedState(BoardViewState):
    def __init__(self, game, character_selected):
        super().__init__(game)
        self.character_selected = character_selected

        #    Button(900, 100, lambda: self.attack_character_state(), self.game.config.assets.imgs["attack_frame"]),

        self.move_button = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((10, 200), (100, 50)),
            text = 'Move',
            manager= self.game.ui_manager,
        )

        self.cancel_button = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((10, 250), (100, 50)),
            text = 'Cancel',
            manager= self.game.ui_manager,
        )

        self.buttons = {
            self.move_button: self.move_character_state,
            self.cancel_button: self.cancel_character_state
        }

    def handle_button_pressed(self, event):
        button_clicked = self.buttons.get(event.ui_element)
        if button_clicked:
            button_clicked()

    # Button commands

    def move_character_state(self):
        print("MOVE BUTTON CLICKED!!!")
        if self.player_turn == self.character_selected.player_id \
        and self.character_selected.moved == False:
            print("switching to CharacterMoveState")
            self.game.change_state(CharacterMoveState(self.game, self.character_selected))
        elif self.player_turn != self.character_selected.player_id:
            print("it is not your turn to move characters")
        else:
            print("this character has already used its move this turn")

    def attack_character_state(self):
        self.game.change_state(CharacterMoveState(self.game, self.character_selected))

    def cancel_character_state(self):
        self.game.change_state(BoardIdleState(self.game))

    def draw(self):
        super().draw()

    def cleanup(self):
        for button in self.buttons:
            button.kill()


class CharacterMoveState(BoardViewState):
    def __init__(self, game, character_selected):
        super().__init__(game)
        self.character_selected = character_selected

        self.cancel_button = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((10, 250), (100, 50)),
            text = 'Cancel',
            manager= self.game.ui_manager,
        )

        self.buttons = {
            self.cancel_button: self.cancel_character_state
        }

    def handle_button_pressed(self, event):
        button_clicked = self.buttons.get(event.ui_element)
        if button_clicked:
            button_clicked()

    def handle_click(self, x, y):
        object_type, clicked_object = self.renderer.check_click(x, y, self.game.board)
        if object_type == "TILE":
            print("CHARACTER STATE IS MOVE AND A TILE WAS CLICKED")
            self.move_character(clicked_object)

    def move_character(self, new_tile):
        print("MOVING TEST (CLIENT -> SERVER)")
        message_id = f"{self.game.player_id}_{self.game.message_counter}"
        col = int(new_tile.col)
        row = int(new_tile.row)
        char_id = int(self.character_selected.character_id)
        print(f"ID: {message_id} COL: {col} ROW:{row}, char_id: {char_id}")
        msg = {"action": "MOVE",
                          "new_col": col,
                          "new_row": row,
                          "character_id": char_id,
                          "message_id": message_id}

        self.game.send_to_server(msg, message_id)
        self.game.change_state(BoardIdleState(self.game))  # return to idle state
        #self.board.move_character(self.character_selected, new_tile)

    # Button commands

    def cancel_character_state(self):
        self.game.change_state(BoardIdleState(self.game))

    def cleanup(self):
        for button in self.buttons:
            button.kill()

###############################
# ATTACK CLASS NOT FUNCTIONAL #
###############################

class CharacterAttackState(BoardViewState):
    def __init__(self, game, character_attacked):
        super().__init__(game)
        self.character_attacked = character_attacked
        self.buttons = [Button(900, 300, lambda: self.game.open_board(), self.game.config.assets.imgs["cancel_frame"])]

    def draw(self):
        super().draw()
        for button in self.buttons:
            self.window.blit(button.img, (button.x, button.y))

    def attack_character(self, tile):
        print("ATTACKING TEST")
        # print(vars(tile))
        # col, row = tile.col, tile.row  # NEED TO FIX THIS SO IT'S NOT SWAPPED
        # self.board.characters[0].row = row
        # self.board.characters[0].col = col

