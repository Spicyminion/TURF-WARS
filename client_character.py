class Character:
    def __init__(self, img_key, col, row, character_id, player_id, attack_abilities, passive_abilities,
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
        self.items = []
        self.attack_abilities = passive_abilities
        self.passive_abilities = attack_abilities

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

class Vehicle:
    def __init__(self, img_key, col, row, vehicle_id, player_id, abilities,
                 hp=10, dmg=1, movement_range=2, capacity=2):
        self.hp = hp
        self.damage = dmg
        self.movement_range = movement_range
        self.capacity = capacity
        self.img_key = img_key
        self.col = col
        self.row = row
        self.vehicle_id = vehicle_id
        self.player_id = player_id
        self.abilities = list(abilities)
        self.moved = False

