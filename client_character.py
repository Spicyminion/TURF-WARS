
class Character:
    def __init__(self, hp, dmg, img_key, col, row, id):
        self.x = None
        self.y = None
        self.hp = hp
        self.damage = dmg
        self.img_key = img_key
        self.col = col
        self.row = row
        self.id = id
        self.moved = False
        self.options = False
        self.items = []

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col

    def action_list(self):
        action = None






