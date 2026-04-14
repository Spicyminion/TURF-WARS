

class Shop:
    def __init__(self, window):
        self.characters = {
            "test": {"health": "10", "cost": 200}
        }
        self.window = window

    #def initialize_shop(self):
    #    for character in self.characters.values():

    def check_click(self, x, y, *args):
        print("shop click not functional yet")

    def draw(self):
        self.window.fill((255,255,255))


    def purchase_character(self, character):
        pass


    def shop_button(self, x, y):
        pass

