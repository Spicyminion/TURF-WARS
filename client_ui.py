import pygame

class UI:
    def __init__(self, window):
        self.window = window
        self.start_buttons = []
        self.board_buttons = []
        self.action_buttons = []
        self.shop_buttons = []
        self.state = "BOARD"
        self.click_check = {
            "BOARD": lambda: self.board_buttons,
            "CHARACTER_SELECTED": lambda: self.board_buttons + self.action_buttons,
            "SHOP": lambda: self.shop_buttons,
            "START": lambda: self.start_buttons
        }

    def draw(self):
            for button in self.click_check[self.state]():
                self.window.blit(button.img, (button.x, button.y))

    def check_click(self, x, y, state):
        status = False
        for button in self.click_check[state]():
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
            pass
        elif click_x - self.x < 0 or click_y - self.y < 0:
            pass
        else:
            check_x, check_y = (click_x - self.x, click_y - self.y)
            if self.mask.get_at((round(check_x), round(check_y))):
                print("BUTTON PRESSED")
                self.command()