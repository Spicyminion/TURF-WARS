import pygame
import socket
import threading
from turf_network import Network
from turf_server import IP
from client_game import Game
from client_config import ConfigGame

#####################
# Initialize Client #
#####################

class Client:
    def __init__(self, ip):
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP protocol, data transfer protocol
        self.connect_to_server(self.ip)

    def connect_to_server(self, ip):
        print("Connecting to server")
        self.client.connect((ip, 5555))
        self.client.send(str.encode("hello"))
        threading.Thread(target=self.maintain_conn).start()

    def maintain_conn(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    print("Connection closed")
                    break
                print(f"new message: {data}")
            except ConnectionResetError:
                print("Server crashed")
                break

    def send(self, action):
        print("sending action")
        self.client.send(str.encode(action))



person = Client(IP)


#######################################
# Load assets for the board rendering #
#######################################

pygame.init()
pygame.display.set_caption("TURF WARS")
res = pygame.display.Info()
config = ConfigGame(res.current_w, res.current_h)
SCREEN = pygame.display.set_mode((config.screen_width, config.screen_height))
config.load_imgs()

######################################################
# Main loop for continuously checking for new inputs #
######################################################

clock = pygame.time.Clock()
FPS = 60
NUM_OF_PLAYERS = 2

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
                    print("### CLICK ###")
                    game.check_pos(x, y)

                elif event.button == 2:
                    pass

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game.zoom(1)
                    print("zooming in")
                    person.send("ZOOM")  # Test to see if server receives message
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