from enum import Enum
# 7x7 grid
# 1D is x-axis, 2D is y-axis (they are printed diagonally downwards from R to L) * imagine array rotated 45 deg. left
# 0 = blank space, 1 = base, 2 = spawn_circle, 3 = lock_space, 4 = house, 5 = mall



class TileType(Enum):
    BLANK = 0
    BASE = 1
    SPAWN_CIRCLE = 2
    LOCK_SPACE = 3
    HOUSE = 4
    MALL = 5

TILETYPE_TO_SPRITE = {
    TileType.BLANK: "grass_block",
    TileType.BASE: "clicked_block",
    TileType.SPAWN_CIRCLE: "clicked_block",
    TileType.LOCK_SPACE: "clicked_block",
    TileType.HOUSE: "clicked_block",
    TileType.MALL: "clicked_block",
}


layout = [
    [TileType.BASE,         TileType.SPAWN_CIRCLE,  TileType.BLANK,     TileType.LOCK_SPACE,    TileType.BLANK, TileType.SPAWN_CIRCLE,  TileType.BASE,],
    [TileType.SPAWN_CIRCLE, TileType.BLANK,         TileType.BLANK,     TileType.BLANK,         TileType.BLANK, TileType.BLANK,         TileType.SPAWN_CIRCLE,],
    [TileType.BLANK,        TileType.BLANK,         TileType.HOUSE,     TileType.BLANK,         TileType.HOUSE, TileType.BLANK,         TileType.BLANK, ],
    [TileType.LOCK_SPACE,   TileType.BLANK,         TileType.BLANK,     TileType.MALL,          TileType.BLANK, TileType.BLANK,         TileType.LOCK_SPACE, ],
    [TileType.BLANK,        TileType.BLANK,         TileType.HOUSE,     TileType.BLANK,         TileType.HOUSE, TileType.BLANK,         TileType.BLANK, ],
    [TileType.SPAWN_CIRCLE, TileType.BLANK,         TileType.BLANK,     TileType.BLANK,         TileType.BLANK, TileType.BLANK,         TileType.SPAWN_CIRCLE, ],
    [TileType.BASE,         TileType.SPAWN_CIRCLE,  TileType.BLANK,     TileType.LOCK_SPACE,    TileType.BLANK, TileType.SPAWN_CIRCLE,  TileType.BASE],
]

'''
layout = [
    [1, 2, 0, 3, 0, 2, 1,],
    [2, 0, 0, 0, 0, 0, 2,],
    [0, 0, 4, 3, 4, 0, 0,],
    [3, 0, 3, 5, 3, 0, 0,],
    [0, 0, 4, 3, 4, 0, 0,],
    [2, 0, 0, 0, 0, 0, 2,],
    [1, 2, 0, 3, 0, 2, 1,]
]

'''