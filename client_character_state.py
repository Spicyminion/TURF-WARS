from client_board_state import BoardIdleState
from client_game import GameState
from client_ui import Button, HUD

class CharacterSelected(GameState):
    def __init__(self, game, character_selected):
        super().__init__(game)
        self.character_selected = character_selected

        self.buttons = [
            Button(900, 10, lambda: self.move_character_state(), self.game.config.assets.imgs["attack_frame"]),
            Button(900, 100, lambda: self.attack_character_state(), self.game.config.assets.imgs["move_frame"]),
            Button(900, 300, lambda: self.game.open_board(), self.game.config.assets.imgs["cancel_frame"])
        ]

    def handle_click(self, x, y):
        for button in self.buttons:
            if button.check_mask(x, y):
                button.command()
                status = True

    def move_character_state(self):
        self.game.change_state(CharacterMoveState(self.game, self.character_selected))

    def attack_character_state(self):
        self.game.change_state(CharacterMoveState(self.game, self.character_selected))

    def cancel_character_state(self):
        self.game.change_state(BoardIdleState(self.game))

class CharacterMoveState(GameState):
    def __init__(self, game, character_moved):
        super().__init__(game)
        self.character_moved = character_moved

        self.buttons = [Button(900, 300, lambda: self.game.open_board(), self.game.config.assets.imgs["cancel_frame"])]

    def handle_click(self, x, y):
        status = False
        for button in self.buttons:
            if button.check_mask(x, y):
                button.command()
                status = True
                break
        #if status == False and :


    def cancel_character_state(self):
        self.game.change_state(BoardIdleState(self.game))


    def move_character(self, new_tile):
        print("MOVING TEST")
        #print(vars(tile))
        old_tile = self.board.tiles[self.selected_char.col][self.selected_char.row]
        old_tile.characters.remove(self.selected_char)

        self.selected_char.row = new_tile.row
        self.selected_char.col = new_tile.col

        new_tile = self.board.tiles[self.selected_char.col][self.selected_char.row]
        new_tile.characters.append(self.selected_char)

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
