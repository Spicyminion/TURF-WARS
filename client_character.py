from client_game import GameState

class Character:
    def __init__(self, hp, dmg, img_key, col, row, id):
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

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            print("aRIPgus, ur dead")

    def add_item(self, item):
        if len(self.items) < 2:
            self.items.append(item)

class CharacterSelectedState(GameState):
    pass





