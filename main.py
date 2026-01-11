import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_OFFSET_X, INITIAL_OFFSET_Y, HALF_HEIGHT, HALF_WIDTH)

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

################################################
# Func for determining which tile is L_clicked #
################################################

def calc_tile_coord(position):

    # First we need to center the coordinates with respect to top of board
    x, y = position
    cx, cy = x - INITIAL_OFFSET_X - HALF_WIDTH, y - INITIAL_OFFSET_Y

    # Now normalize x & y coords to width and height of each tile respectively (units for moving)
    nx = cx / HALF_WIDTH
    ny = cy / HALF_HEIGHT

    # Next convert into x, y within range of (7,7) 7x7 tiles
    gx = (nx + ny) / 2
    gy = (ny - nx) / 2

    # Compute which tile is being used
    row = int(gx)
    col = int(gy)

    print(f"norm_x,norm_y: {nx, ny}")
    print(f"x,y: {row, col}")


#######################################################
# Main loop for continuously checking for new  inputs #
#######################################################

clock = pygame.time.Clock()
FPS = 60

def main():

    running = True
    while running:

        clock.tick(FPS)
        SCREEN.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # event == 1 is L_click, == 2 is middle_button, == 3, is R_click

                if event.button == 1:
                    location = pygame.mouse.get_pos()
                    calc_tile_coord(location)

            elif event.type == pygame.QUIT:
                running = False

            pygame.display.flip()


        pygame.quit()

main()