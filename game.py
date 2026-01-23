import pygame
from board import Board, UI
from player import PlayerCamera
from tile import Button
class Game:

    def __init__(self, window, config):
        self.window = window
        self.config = config
        self.players = []
        self.cameras = []
        self.player_turn = 1
        self._init()

    def _init(self):
        self.board = Board(self.window, self.config)
        self.ui = UI()
        self.ui.buttons.append(Button(10, 10, self.change_turn()))
        #self.ui.draw_buttons(self.window)

    def draw_camera(self, player_turn):
        self.cameras[player_turn-1].draw_all()  # -1 for 0-based indexing

    def update(self):
        self.cameras[self.player_turn-1].draw_all()

    def get_button(self, x, y):
        self.ui.check_buttons(x, y)

    def check_pos(self, x, y, ):



    def check_all(self, d1, d2, x, y ):
        for build in self.board.tiles[d1][d2].building:
            if build.check_click(x, y):
                build.draw_stat(self.window)
    '''
    def make_cameras(self):
        for player in self.players:
            self.cameras.append(PlayerCamera(
                player, self.window, self.config, self.board,
                self.config.INITIAL_OFFSET_X, self.config.INITIAL_OFFSET_Y, self.config.HALF_WIDTH, self.config.HALF_HEIGHT))
        self.draw_camera(1)

    def zoom(self, zoom):
        cam = self.cameras[self.player_turn-1]
        check = cam.zoom_level + zoom
        if check < 1 or check > 3:
            pass
        else:
            cam.zoom_level+=zoom
            cam.update_imgs()

    def move_y(self, increment):
        cam = self.cameras[self.player_turn-1]
        cam.camera_offset_y += increment
        cam.update_imgs()

    def move_x(self, increment):
        cam = self.cameras[self.player_turn-1]
        cam.camera_offset_x += increment
        cam.update_imgs()

    def rotate(self, direction):
        cam = self.cameras[self.player_turn-1]
        check = cam.camera_rotation_offset + direction
        if check > 3:
            cam.camera_rotation_offset = 0
        elif check < 0:
            cam.camera_rotation_offset = 3
        else:
            cam.camera_rotation_offset += direction
        cam.update_imgs()

    def change_turn(self):
        if self.player_turn == len(self.players):
            self.player_turn = 1
        else:
            self.player_turn += 1

    def center_board(self):
        cam = self.cameras[self.player_turn-1]
        cam.center_board()

    def draw_board(self):

'''
class MoveCommand():
    def __init__(self):
'''