# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50005              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    response = ""
    while response != "escaped" and response != "dead":
        command = input(">> ")
        client_socket.send(command.encode())
        data = client_socket.recv(1024)
        response = data.decode()
        print(response)
    client_socket.close()
