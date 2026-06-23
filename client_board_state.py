import pygame
from client_game import GameState
from client_board_renderer import BoardRenderer
from client_character import Character


class BoardIdleState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.renderer = game.renderer
        self.board = game.board
        self.camera = game.camera

    def handle_click(self, x, y):
        object_type, clicked_object = self.renderer.check_click(x, y, self.board) # renderer will handle what is clicked
        if clicked_object == type(Character):
            self.game.open_character(clicked_object)

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

    def draw(self):
        self.renderer.draw(self.board)
