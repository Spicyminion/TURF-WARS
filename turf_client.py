import pygame
import socket
from turf_network import Network
from turf_server import IP
from client_config import ConfigGame
width = 500
height = 500

pygame.init()

# Check resolution of local computer
res = pygame.display.Info()
config = ConfigGame(res.current_w, res.current_h)
SCREEN = pygame.display.set_mode((config.screen_width, config.screen_height))
config.load_imgs()

class Client:
    def __init__(self, ip):
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IP protocol, data transfer protocol
        self.connect_to_server(self.ip)

    def connect_to_server(self, ip):
        print("Connecting to server")
        self.client.connect((ip, 5555))
        self.client.send(str.encode("hello"))
        self.maintain_conn()

    def maintain_conn(self):
        while True:
            msg = input()
            if msg == "exit":
                break
            self.client.send(str.encode(msg))


person = Client(IP)