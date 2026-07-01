import json
import pygame
import time
import socket
import threading
import queue
from turf_network import Network
from turf_server import IP
from client_game import Game
from client_config import ConfigGame
import pygame
import pygame_gui

##########################
# Initialize Game Object #
##########################

message_list = queue.Queue() # this will keep track of messages for the client to pass to game obj

pygame.init()
res = pygame.display.Info()
config = ConfigGame(res.current_w, res.current_h)
SCREEN = pygame.display.set_mode((config.screen_width, config.screen_height))
config.load_imgs()

clock = pygame.time.Clock()
FPS = 60
NUM_OF_PLAYERS = 2

manager = pygame_gui.UIManager((config.screen_width, config.screen_height), theme_path="custom_buttons.json")

"""
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)
"""

#game = Game(SCREEN, config, NUM_OF_PLAYERS)

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
        #self.client.send(str.encode("hello"))
        threading.Thread(target=self.maintain_conn).start()

    def maintain_conn(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    print("Connection closed")
                    break
                print(f"new message: {data}")
                msg = json.loads(data) # convert to python dict
                message_list.put(msg)

            except ConnectionResetError:
                print("Server crashed")
                break

    def send(self, action):
        print("sending action")
        self.client.send(action)


client = Client(IP)

game = Game(SCREEN, config, manager, client, message_list, NUM_OF_PLAYERS)

######################################################
# Main loop for continuously checking for new inputs #
######################################################

def main():
    running = True

    while running:

        time_delta = clock.tick(FPS) / 1000  # <- x/1000 to convert m/s -> s
        pygame.display.flip()

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)  # handle GUI clicks first

            #if event.type == pygame_gui.UI_BUTTON_PRESSED:
            #    if event.ui_element == hello_button:
            #        print("Hello!!!")
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                game.check_buttons_pressed(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # event == 1 is L_click, == 2 is middle_button, == 3, is R_click
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    print("### CLICK ###")
                    game.check_pos(x, y)

                elif event.button == 2:
                    pass

            elif event.type == pygame.KEYDOWN:
                print("### KEY DOWN ###")
                game.check_key_pressed(event.key)

        keys = pygame.key.get_pressed()
        game.game_state.handle_continuous_inputs(keys)

        game.update()
        manager.update(time_delta)

        SCREEN.fill((255,255,255))

        game.draw_screen()
        manager.draw_ui(SCREEN)
        pygame.display.flip()

    pygame.quit()

main()