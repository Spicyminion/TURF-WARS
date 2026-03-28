# JSON - JavaScript Object Notation
import json
import socket
from network import Network
import threading

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

# First make a server

addr = ("192.168.1.95", 5555)  # Server IP, Port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket that can connect to IPV4 , TCP connection
server.bind(addr) # assign the socket
server.listen(5)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(addr)
conn, addr = server.accept()    # conn is how the server will communicate with the client
print(conn)


client.send(str.encode("hello"))
msg = conn.recv(1024).decode()
print(msg)


def chat_test():
    while True:
        msg = input("send a message: ")
        client.send(str.encode(msg))
        if msg == 'exit':
            break

threading.Thread(target=chat_test).start()

while True:
    msg = conn.recv(1024).decode()
    if msg == 'exit':
        print("goodbye")
        conn.close()
        break
    else:
        print(f"the message is: {msg}")

#lient.send(new_json.encode("utf-8"))

exit()

class Player:
    def __init__(self, name):
        self.name = name

def main():
    run = True
    n = Network() # We will contain all client <-> server commands in this object to use
    player = Player("WUP")

main()