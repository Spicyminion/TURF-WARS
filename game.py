import pygame
from pygame.mixer_music import get_pos

pygame.init()

screen = pygame.display.set_mode((800, 800))
COLOR_KEY = (0,0,0)
test_2 = pygame.image.load('grass_block.png').convert()
test_2.set_colorkey(COLOR_KEY)
# size is 51 x 51
running = True
clock = pygame.time.Clock()

while running:

    screen.fill((255,255,255))
    screen.blit(test_2,(400, 0))
    screen.blit(test_2,(425, 13))
    screen.blit(test_2,(375, 13))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            location = pygame.mouse.get_pos()
            print(f"clicked at {location}")
        elif event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
