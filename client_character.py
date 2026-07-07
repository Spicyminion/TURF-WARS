class Character:
    def __init__(self, img_key, col, row, character_id, player_id,
                 hp=10, dmg=1, movement_range=1):
        self.hp = hp
        self.damage = dmg
        self.movement_range = movement_range
        self.img_key = img_key
        self.col = col
        self.row = row
        self.character_id = character_id
        self.player_id = player_id
        self.moved = False
        self.options = False
        self.items = []

    def move(self, new_col, new_row):
        self.col = new_col
        self.row = new_row
        self.moved = True

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            print("aRIPgus, ur dead")

    def add_item(self, item):
        if len(self.items) < 2:
            self.items.append(item)

class Bob(Character):
    def __init__(self, img_key, col, row, character_id, player_id, hp=20, dmg=5, movement_range=1):
        super().__init__(img_key, col, row, character_id, player_id,
                         hp=hp, dmg=dmg, movement_range=movement_range)

    def say_hi(self):
        print("Bob says hi")

class Joe(Character):
    def __init__(self, img_key, col, row, character_id, player_id, hp=15, dmg=7, movement_range=1):
        super().__init__(img_key, col, row, character_id, player_id,
                         hp=hp, dmg=dmg, movement_range=movement_range)

class Xub(Character):
    def __init__(self, img_key, col, row, character_id, player_id, hp=20, dmg=2, movement_range=1):
        super().__init__(img_key, col, row, character_id, player_id,
                         hp=hp, dmg=dmg, movement_range=movement_range)

    def say_hi(self):
        print("Joe says hi")
