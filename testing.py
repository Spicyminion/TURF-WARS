# JSON - JavaScript Object Notation
import json
import socket
from network import Network

json_string = '''
    {
        "students": [
            {"id": 1, "name": "WUP"},
            {"id": 2, "name": "SUP"},
            {"id": 3, "name": "XUB"}
        ]
    }
'''

data = json.loads(json_string)  # converts to a python dictionary
data['test'] = True
new_json = json.dumps(data, indent=2, sort_keys=True) # convert python dict to json string (format)

addr = ("192.168.1.95", 5555)  # Server IP, Port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket that can connect to IPV4 , TCP connection
client.connect(addr)

client.send(new_json.encode("utf-8"))

class Player:
    def __init__(self, name):
        self.name = name

def main():
    run = True
    n = Network() # We will contain all client <-> server commands in this object to use
    player = Player("WUP")

main()