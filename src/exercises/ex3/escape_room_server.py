# Escape room server
import socket
import random
import threading
import sys
from escape_room import EscapeRoom

def multithread(conn):
    while True:
        # create an escape room
        escape_room = EscapeRoom()
        escape_room.start()
        # while the escape room status is locked
        # read the data from conn
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

if __name__ == '__main__':

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50001              # Arbitrary non-privileged port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        while True:
            connection,address= server_socket.accept()
            print("listening")
            threading._start_new_thread(multithread,(connection,))
