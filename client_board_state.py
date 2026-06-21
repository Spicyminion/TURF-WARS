from client_game import GameState
from client_board_renderer import BoardRenderer
from client_character import Character


class BoardIdleState(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.game = game
        self.renderer = game.renderer
        self.board = game.board

    def handle_click(self, x, y):
        clicked_object = self.renderer.check_click(x, y, self.board) # renderer will handle what is clicked
        if clicked_object == type(Character):
            self.game.open_character(clicked_object)
