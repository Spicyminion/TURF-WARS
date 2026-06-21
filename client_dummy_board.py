from layout import layout, TileType, BuildType
from client_tile import Tile, Building
from client_dummy_tiles import Tile, Building
from client_character import Character

# Purely store tiles, buildings and characters in this object (no rendering, movement, etc.)

class DummyBoard:

    def __init__(self):
        self.tiles = []
        self.buildings = []
        self.characters = []
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
                    tile.building = Building(column, row, BuildType.APARTMENT, 1)  # for testing purposes
        #self.add_object(3, 3, "CHARACTER", 1)

    def add_object(self, col, row, object_type):
        pass
        # Add code later
        #tile = self.tiles[int(col)][int(row)]




