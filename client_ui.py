import pygame

class HUD:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.config = game.config
        self.permanent_buttons = []
        self.character_buttons = []
        self.start_buttons = []
        self.board_buttons = []
        self.shop_buttons = []

        # PERMANENT OVERLAY BUTTONS
        #self.permanent_buttons.append(Button(10, 10, self.game.change_turn, self.config.assets.imgs["change_turn"]))
        #self.permanent_buttons.append(Button(10, 100, lambda: self.game.change_state(self.), self.config.assets.imgs["shop"]))  # <- ADD LATER
        self.permanent_buttons.append(Button(10, 10, lambda: self.game.open_board(), self.config.assets.imgs["board"]))


    def draw(self, state):
            for button in self.permanent_buttons:
                self.window.blit(button.img, (button.x, button.y))
            for button in state:
                self.window.blit(button.img, (button.x, button.y))

    def draw_hud(self):
        pass # might not need this method

    def check_click(self, x, y, state):
        status = False
        for button in self.permanent_buttons:
            if button.check_mask(x, y):
                button.command()
                status = True
                break
        for button in state:
            if button.check_mask(x, y):
                button.command()
                status = True
                break
        return status

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

