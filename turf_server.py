import socket
import json
from _thread import *

#import sys
DESKTOP = "192.168.1.95" # desktop
LAPTOP = "192.168.32.1" # laptop

server = DESKTOP
port = 5555  # where computer directs traffic

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) # assign the socket to a specific IPV4 addr and port #
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

#def threaded_client(conn, addr):

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    try:
        msg = conn.recv(2048).decode("utf-8")
        if not msg:
            print("No data")
            conn.close()
            continue
        else:
            msg = json.loads(msg) # convert back to python dict
            print("Received:", msg)
    except:
        break
    #start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

