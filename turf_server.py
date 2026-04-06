import socket
import json
import threading
from turf_game import Game
#import sys

DESKTOP = "192.168.1.95" # desktop
LAPTOP = "192.168.32.1" # laptop
IP = DESKTOP # changes depending on where we're running the server from

#game = Game()

def run_client(addr, conn):
    while True:
        # will wait on msg line till a new msg received
        try:
            msg = conn.recv(1028).decode()  # conn is what socket to listen to
            if not msg: # msg is empty
                print("Client disconnected")
                break
            print(f"the message is {msg}!")
            conn.send(str.encode("default reply :|"))
        except socket.error as e:
            print(f"socket error: {e}")
            break

def boot_server(ip):

    server = ip
    port = 5555  # where computer directs traffic to internally

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (IP_type , data stream type)  (define type of socket)

    # Now try to start the socket

    try:
        s.bind((server, port)) # assign the socket to a specific IPV4 addr and port num.
    except socket.error as e:
        str(e)

    s.listen(2)  # accept up to 2 clients
    print("Waiting for a connection, Server Started")

    # Now we'll run a constant loop to process new clients

    player_num = 1
    while True:
        conn, addr = s.accept() # will wait here till we get a new client
        print(f"Connection Accepted: {conn} {addr}")

        # Send the client to a thread so it's constantly handled

        threading.Thread(target=run_client, args=(addr,conn)).start()

        player_num+=1


if __name__ == "__main__":
    boot_server(IP)