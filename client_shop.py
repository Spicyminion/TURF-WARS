from client_ui import Button

class Shop:
    def __init__(self, window, config):
        self.characters = {
            "test1": {"health": "10", "cost": 200},
            "test2": {"health": "10", "cost": 200},
            "test3": {"health": "10", "cost": 200}
        }
        self.window = window
        self.config = config
        self.imgs = self.config.assets.imgs
        self.frames = []
        self.initialize_shop()

    def initialize_shop(self):
        rows = 3
        cols = 4
        frame_height = self.imgs["test_char_frame"].get_height()
        frame_width = self.imgs["test_char_frame"].get_width()
        start_x = (self.config.screen_width / 2) - (frame_width * (cols / 2))
        start_y = (self.config.screen_height / 2) - (frame_width * (rows / 2))

        for num in range(rows):
            for num2 in range(cols):
                frame_x = start_x + (num2 * frame_width)
                frame_y = start_y + (num * frame_height)
                self.frames.append(Button(frame_x, frame_y, self.purchase_character, self.imgs["test_char_frame"]))

    def check_click(self, x, y, turn):
        status = False
        for frame in self.frames:
            if frame.check_mask(x, y):
                return

    def draw(self):
        self.window.fill((44,215,247))
        for frame in self.frames:
            self.window.blit(frame.img, (frame.x, frame.y))

    def purchase_character(self):
        print("Purchase character... [NON FUNCTIONAL]")


    def shop_button(self, x, y):
        pass

