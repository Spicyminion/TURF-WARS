import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1800, 900))

scale_factor = 4.0
COLOR_KEY = (0,0,0)
block = pygame.image.load('grass_block.png').convert()
w, h = block.get_size()
block = pygame.transform.scale(block,(int(w * scale_factor), int(h * scale_factor)))
clicked_block = pygame.image.load('clicked_grass_block.png').convert()
block.set_colorkey(COLOR_KEY)
clicked_block.set_colorkey(COLOR_KEY)

# size is 51 x 51
clock = pygame.time.Clock()
HALF_HEIGHT = 12 * scale_factor  # offset dim (half of diamond)
HALF_WIDTH =  25 * scale_factor  # offset dim (half of width)
DIMENSION = 7

INITIAL_OFFSET_X = screen.get_width() / 2 - HALF_WIDTH
INITIAL_OFFSET_Y = (screen.get_height() / 2) - (HALF_HEIGHT * 2 * DIMENSION / 2)
FPS = 60
block_list = []
#row_length = 1


for i in range(DIMENSION):
    block_list.append([])
    for j in range(DIMENSION):
        block_list[i].append(0)

running = True
while running:

    screen.fill((255,255,255))
    x = 0 # row we're on
    for group in block_list:
        for tile in range(DIMENSION):
            # tiles are downwards left per column
            x_coord = INITIAL_OFFSET_X + (HALF_WIDTH * x) - HALF_WIDTH * tile
            y_coord = INITIAL_OFFSET_Y + (HALF_HEIGHT * x) + HALF_HEIGHT * tile
            if block_list[x][tile] == 1:
                screen.blit(clicked_block, (x_coord, y_coord))
            else:
                screen.blit(block, (x_coord, y_coord))
        x += 1


    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()
            print(f"clicked at {location}")

            # Compensate for initial shift (width shift is since tile is generated from a square not diamond)
            #mx, my = location[0] - INITIAL_OFFSET - HALF_WIDTH, location[1] - INITIAL_OFFSET
            mx, my = location[0] - INITIAL_OFFSET_X - HALF_WIDTH, location[1] - INITIAL_OFFSET_Y

            # Normalize x & y coords
            sx = mx / HALF_WIDTH
            sy = my / HALF_HEIGHT

            gx = (sx + sy) / 2
            gy = (sy - sx) / 2

            row = int(gx)
            col = int(gy)

            print(f"mx,my: {mx,my}")
            print(f"x,y: {row, col}")
        elif event.type == pygame.QUIT:
            running = False

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
