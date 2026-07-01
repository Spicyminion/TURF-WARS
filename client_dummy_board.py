from layout import layout, TileType, BuildType
from client_dummy_tiles import Tile, Building
from client_character import Character

# Purely store tiles, buildings and characters in this object (no rendering, movement, etc.)

class DummyBoard:

    def __init__(self):
        self.tiles = []
        self.buildings = {}
        self.characters = {}
        self.define_grid()
        self.player_turn = 1

    def define_grid(self):
        for column in range(len(layout)):
            self.tiles.append([])
            for row in range(len(layout[column])):
                tile_type = layout[column][row]
                self.tiles[column].append(Tile(tile_type, column, row)) # true center
                if column == 1 and row == 1:
                    tile = self.tiles[column][row]
                    tile.building = Building( BuildType.APARTMENT, column, row, 1)  # for testing purposes
        test_character = Character(10, 10, "smile", 3, 3, 1,1,1)
        self.tiles[3][3].characters.append(test_character)
        self.characters = {test_character.character_id: test_character}

    def add_object(self, col, row, object_type):
        pass
        # Add code later
        #tile = self.tiles[int(col)][int(row)]

    def move_character(self, character_id, new_col, new_row):
        character = self.characters[character_id]
        new_tile = self.tiles[new_col][new_row]
        distance = abs(int(character.col) - int(new_tile.col)) + abs(int(character.row) - int(new_tile.row))
        if distance <= character.movement_range:
            old_tile = self.tiles[character.col][character.row]
            old_tile.characters.remove(character)
            new_tile.characters.append(character)
            character.move(new_tile.col, new_tile.row)
            return True
        else:
            print("movement range too far for character")
            return False


    def attack_character(self, character, damage):
        pass



