
class Character:
    def __init__(self, hp, dmg, img_key, row, col):
        self.x = None
        self.y = None
        self.hp = hp
        self.damage = dmg
        self.img_key = img_key
        self.row = row
        self.col = col
        self.moved = False
        self.options = False
        self.items = []

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col

    def action_list(self):
        pass






