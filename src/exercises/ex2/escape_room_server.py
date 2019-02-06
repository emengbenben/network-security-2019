# Escape room server
import socket
import random
from escape_room import EscapeRoom

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50001              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    while True:
        conn, addr = server_socket.accept()
        # create an escape room
        escape_room = EscapeRoom()
        escape_room.start()
        # while the escape room status is locked
        # read the data from conn
        with conn:
            print('Connected by', addr)
            while escape_room.status() == "locked":
                data = conn.recv(1024)
                output = escape_room.command(data.decode())  # encode converts from bytes to string
                # send the output.encode() to conn (encode converts from string to bytes)
                conn.send(output.encode())
            #data = conn.recv(1024)
            #output = escape_room.command(data.decode())
            #conn.send(output.encode())
            if escape_room.status() == "escaped" or escape_room.status() == "dead":
                conn.send(("\n"+escape_room.status()).encode())
            conn.close()
