import pygame
from constants import INITIAL_OFFSET_X, INITIAL_OFFSET_Y, HALF_HEIGHT, HALF_WIDTH, DIMENSION, SCREEN_HEIGHT, SCREEN_WIDTH
from game import Game

###############################
# Init screen and load assets #
###############################

pygame.init()

# Check resolution of local computer
res = pygame.display.Info()

SCREEN = pygame.display.set_mode((res.current_w, res.current_h-50))

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

    return row, col


######################################################
# Main loop for continuously checking for new inputs #
######################################################

clock = pygame.time.Clock()
FPS = 60

def main():

    running = True
    SCREEN.fill((255, 255, 255))
    game = Game(SCREEN)  # initialize game

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # event == 1 is L_click, == 2 is middle_button, == 3, is R_click

                if event.button == 1:
                    location = pygame.mouse.get_pos()
                    d1, d2 = calc_tile_coord(location)
                    if  0 <= d1 <= (DIMENSION-1) and 0 <= d2 <= (DIMENSION-1):
                        print(f"x,y: {d1, d2}")
                        game.get_space(d1, d2, location[0], location[1])

            elif event.type == pygame.QUIT:
                running = False

            pygame.display.flip()

        SCREEN.fill((255,255,255))
        game.update()

    pygame.quit()

main()