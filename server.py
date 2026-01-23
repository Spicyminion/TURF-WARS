import socket
from _thread import *
import sys
# 192.168.1.95 # desktop
# 192.168.32.1 # laptop

SERVER = "192.168.1.95"
port = 5555  # where computer directs traffic

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for some bubbie...")

def threaded_client(conn):

    reply = ""
    while True:
        try:
            conn.send(str.encode("Connected"))

            data = conn.recv(2048) # amount info in bits we can receive
            reply = data.decode("utf-8")    # info needs to be encoded before being sent (human-readable -> computer)

            if not data:
                print("Disconnected")
                break
            else:
                print("Received:", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))

        except:
            break

    print("Connection closed")
    conn.close()


while True:
    conn, addr = s.accept() # returns a new listening socket and the IP of the client
    print("connected to:", addr)

    start_new_thread(threaded_client, (conn,))
