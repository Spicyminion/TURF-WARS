from client_board_state import BoardIdleState
from client_game import GameState
from client_ui import Button, HUD

class CharacterSelectedState(GameState):
    def __init__(self, game, character_selected):
        super().__init__(game)
        self.game = game
        self.window = game.window
        self.camera = game.camera
        self.character_selected = character_selected
        self.renderer = game.board_renderer
        self.buttons = [
            Button(900, 10, lambda: self.move_character_state(), self.game.config.assets.imgs["attack_frame"]),
            Button(900, 100, lambda: self.attack_character_state(), self.game.config.assets.imgs["move_frame"]),
            Button(900, 300, lambda: self.game.open_board(), self.game.config.assets.imgs["cancel_frame"])
        ]

    def handle_click(self, x, y):
        button_clicked = None
        for button in self.buttons:
            if button.check_mask(x, y):
                button_clicked = button
                break
        if button_clicked is not None:
            button_clicked.command()

    # Button commands #

    def move_character_state(self):
        self.game.change_state(CharacterMoveState(self.game, self.character_selected))

    def attack_character_state(self):
        self.game.change_state(CharacterMoveState(self.game, self.character_selected))

    def cancel_character_state(self):
        self.game.change_state(BoardIdleState(self.game))

    def draw(self):
        self.renderer.draw_board(self.game.board)

class CharacterMoveState(GameState):
    def __init__(self, game, character_selected):
        super().__init__(game)
        self.character_selected = character_selected
        self.renderer = game.board_renderer
        self.board = game.board
        self.buttons = [Button(900, 300, lambda: self.game.open_board(), self.game.config.assets.imgs["cancel_frame"])]

    def handle_click(self, x, y):
        button_clicked = None
        for button in self.buttons:
            if button.check_mask(x, y):
                button_clicked = button
                break
        if button_clicked is not None:
            button_clicked.command()
        else:
            object_type, clicked_object = self.renderer.check_click(x, y, self.game.board)
            if object_type == "TILE":
                self.move_character(clicked_object)

    def move_character(self, new_tile):
        print("MOVING TEST")
        old_tile = self.board.tiles[self.character_selected.col][self.character_selected.row]
        old_tile.characters.remove(self.character_selected)

        self.character_selected.row = new_tile.row
        self.character_selected.col = new_tile.col

        new_tile = self.board.tiles[self.character_selected.col][self.character_selected.row]
        new_tile.characters.append(self.character_selected)

        self.game.change_state(BoardIdleState(self.game)) # return to idle state

    # Button commands

    def cancel_character_state(self):
        self.game.change_state(BoardIdleState(self.game))


class CharacterAttackState(GameState):
    def __init__(self, game, character_attacked):
        super().__init__(game)
        self.character_attacked = character_attacked

    def attack_character(self, tile):
        print("ATTACKING TEST")
        # print(vars(tile))
        # col, row = tile.col, tile.row  # NEED TO FIX THIS SO IT'S NOT SWAPPED
        # self.board.characters[0].row = row
        # self.board.characters[0].col = col
