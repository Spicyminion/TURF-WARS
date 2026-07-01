import pygame
import pygame_gui
import json

class HUD:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.config = game.config
        self.permanent_buttons = []

        """
        # PERMANENT OVERLAY BUTTONS
        self.permanent_buttons.append(Button(10, 200, self.game.change_turn, self.config.assets.imgs["change_turn"])) # <- ADD LATER
        self.permanent_buttons.append(Button(10, 100, lambda: self.game.change_state(self.), self.config.assets.imgs["shop"]))  # <- ADD LATER
        self.permanent_buttons.append(Button(10, 10, lambda: self.game.open_board(), self.config.assets.imgs["board"]))
        """

        self.change_turn_button = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((10, 10), (100, 50)),
            text = 'END TURN',
            manager= self.game.ui_manager,
        )

        self.view_board_button = pygame_gui.elements.UIButton(
            relative_rect = pygame.Rect((10, 50), (100, 50)),
            text = 'BOARD',
            manager= self.game.ui_manager,
        )

        self.buttons = {
            self.change_turn_button: self.change_turn,
            self.view_board_button: self.game.open_board
        }

    def handle_button_pressed(self, event): # event is passed from the pygame_gui event manager
        button_clicked = self.buttons.get(event.ui_element)
        if button_clicked:
            button_clicked()

    def cleanup(self):
        for button in self.buttons:
            button.kill()

    def change_turn(self):
        if int(self.game.player_id) == int(self.game.player_turn):
            player_id = self.game.player_id
            message_id = f"{self.game.player_id}_{self.game.message_counter}"
            msg = {"action": "CHANGE_TURN",
                    "player_id": player_id,
                    "message_id": message_id}
            self.game.client.send(json.dumps(msg).encode())
        else:
            print("not your turn to end")
    """
    def draw_hud(self):
            for button in self.permanent_buttons:
                self.window.blit(button.img, (button.x, button.y))
    
    def check_click(self, x, y):
        button_clicked = None
        for button in self.permanent_buttons:
            if button.check_mask(x, y):
                button_clicked = button
                break
        if button_clicked:
            button_clicked.command()
    """

class Button:
    def __init__(self, x, y, command, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = None
        self.command = command
        self.make_mask()

    def make_mask(self):
        self.mask = pygame.mask.from_threshold(self.img, (0, 0, 0), (1, 1, 1, 255))
        self.mask.invert()

    def check_mask(self, click_x, click_y):
        rect = self.img.get_rect(topleft=(self.x, self.y))
        if not rect.collidepoint(click_x, click_y):
            return False
        elif click_x - self.x < 0 or click_y - self.y < 0:
            return False
        else:
            check_x, check_y = (click_x - self.x, click_y - self.y)
            if self.mask.get_at((round(check_x), round(check_y))):
                return True
        return False

