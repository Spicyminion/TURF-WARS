import pygame

# 7x7 grid
# 1D is x-axis, 2D is y-axis (they are printed diagonally downwards from R to L) * imagine array rotated 45 deg. left
# 0 = blank space, 1 = base, 2 = spawn_circle, 3 = lock_space, 4 = house, 5 = mall

layout = [
    [1, 2, 0, 3, 0, 2, 1,],
    [2, 0, 0, 0, 0, 0, 2,],
    [0, 0, 4, 0, 4, 0, 0,],
    [3, 0, 0, 5, 0, 0, 3,],
    [0, 0, 4, 0, 4, 0, 0,],
    [2, 0, 0, 0, 0, 0, 2,],
    [1, 2, 0, 3, 0, 2, 1,],
]