import pygame
from constants import NUM_OF_PLAYERS
from game import Game
from config import ConfigGame
from player import Player

###############################
# Init screen and load assets #
###############################

pygame.init()

# Check resolution of local computer
res = pygame.display.Info()
config = ConfigGame(res.current_w, res.current_h)
SCREEN = pygame.display.set_mode((config.screen_width, config.screen_height))
config.load_imgs()

######################################################
# Main loop for continuously checking for new inputs #
######################################################

clock = pygame.time.Clock()
FPS = 60


def main():

    running = True
    SCREEN.fill((255, 255, 255))
    game = Game(SCREEN, config, NUM_OF_PLAYERS)  # initialize game

    while running:

        pygame.display.flip()

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # event == 1 is L_click, == 2 is middle_button, == 3, is R_click
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    game.check_pos(x, y)

                elif event.button == 2:
                    pass

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game.zoom(1)
                    print("zooming in")
                elif event.key == pygame.K_x:
                    game.zoom(-1)
                    print("zooming out")
                elif event.key == pygame.K_t:
                    game.change_turn()
                elif event.key == pygame.K_r:
                    game.rotate(1)
                elif event.key == pygame.K_c:
                     game.center_board()

            '''         
            else:
                x, y = pygame.mouse.get_pos()
                d1, d2 = calc_tile_coord(x, y)
                if 0 <= d1 <= (DIMENSION - 1) and 0 <= d2 <= (DIMENSION - 1):
                    game.check_all(d1, d2, x, y)
            '''

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            game.move_y(-5)
        elif keys[pygame.K_DOWN]:
            game.move_y(5)
        elif keys[pygame.K_LEFT]:
            game.move_x(-5)
        elif keys[pygame.K_RIGHT]:
            game.move_x(5)

        pygame.display.flip()

        SCREEN.fill((255,255,255))
        game.update()

    pygame.quit()

main()
