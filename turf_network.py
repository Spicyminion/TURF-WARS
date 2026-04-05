import socket
import json

# The network needs to know which port and address to connect to

class Network:
    def __init__(self, hostname):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostname = hostname
        self.server = self.check_address()
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def check_address(self):
        if self.hostname == "DESKTOP":
            return "192.168.1.95"
        elif self.hostname == "LAPTOP":
            return "192.168.32.1"
        return None

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            data = json.dumps(data).encode()
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
