from layout import TileType, TILETYPE_TO_SPRITE, BUILDTYPE_TO_SPRITE

class Tile:
    def __init__(self, tile_type, col, row):
        self.row = row
        self.col = col
        self.type = tile_type
        self.img_key = TILETYPE_TO_SPRITE[tile_type]
        self.characters = []
        self.building = None
        self.id = None

class Building:
    def __init__(self, build_type, col, row, player_id):
        self.row = row
        self.col = col
        self.build_type = build_type
        self.img_key = BUILDTYPE_TO_SPRITE[build_type]
        self.player_id = player_id

class Apartment(Building):
    def __init__(self, build_type, col, row, player_id, revenue):
        super().__init__(build_type, col, row, player_id)
        self.revenue = revenue

    def end_of_turn(self):
        print("printing money WOOO!!!")
        return 500

class OilRig(Building):
    def __init__(self, build_type, col, row, player_id, revenue):
        super().__init__(build_type, col, row, player_id)
        self.revenue = revenue

    def end_of_turn(self):
        print("printing money WOOO!!!")
        self.smog_damage()
        return 250

    def smog_damage(self):
        print("smog currently does nothing")