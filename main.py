import pygame
from constants import HALF_HEIGHT, HALF_WIDTH, DIMENSION
from game import Game
from board import UI
from config import ConfigGame
from player import Player, PlayerCamera

###############################
# Init screen and load assets #
###############################

pygame.init()

# Check resolution of local computer
res = pygame.display.Info()
config = ConfigGame(res.current_w, res.current_h)
SCREEN = pygame.display.set_mode((config.screen_width, config.screen_height))

# Update image sizes


################################################
# Funcs for determining which button or tile is L_clicked #
################################################


def calc_tile_coord(x, y):

    # First we need to center the coordinates with respect to top of board
    cx, cy = x - config.INITIAL_OFFSET_X - config.HALF_WIDTH, y - config.INITIAL_OFFSET_Y

    # Now normalize x & y coords to width and height of each tile respectively (units for moving)
    nx = cx / config.HALF_WIDTH
    ny = cy / config.HALF_HEIGHT

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
    game = Game(SCREEN, config)  # initialize game
    game.players = [Player(1), Player(2)]
    game.make_cameras()
    game.draw_camera(1)
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # event == 1 is L_click, == 2 is middle_button, == 3, is R_click
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    game.check_pos(x, y)

                elif event.button == 2:
                    pass

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game.zoom_in()
                    print("zooming in")
                elif event.key == pygame.K_x:
                    game.zoom_out()
                    print("zooming out")
                elif event.key == pygame.K_UP:
                    game.move_y(-20)
                elif event.key == pygame.K_DOWN:
                    game.move_y(20)
                elif event.key == pygame.K_LEFT:
                    game.move_x(-20)
                elif event.key == pygame.K_RIGHT:
                    game.move_x(20)
                elif event.key == pygame.K_t:
                    game.change_turn()
                elif event.key == pygame.K_r:
                    game.rotate(1)


            elif event.type == pygame.QUIT:
                running = False
            '''
            else:
                x, y = pygame.mouse.get_pos()
                d1, d2 = calc_tile_coord(x, y)
                if 0 <= d1 <= (DIMENSION - 1) and 0 <= d2 <= (DIMENSION - 1):
                    game.check_all(d1, d2, x, y)
            '''

            pygame.display.flip()

        SCREEN.fill((255,255,255))
        game.update()

    pygame.quit()

main()