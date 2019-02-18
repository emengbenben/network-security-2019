import asyncio
import sys
import datetime
import os.path
from pathlib import Path

class ExampleHttpServer(asyncio.Protocol):

    def __init__(self, document_root):
        # initialization
        self.buffer =  bytes()
        self.document_root = document_root

    #check if have a \r\n\r\n
    def has_full_packet(self, buffer):
        buffer_string = buffer.decode()[-4:]
        if  buffer_string == "\r\n\r\n":
            return True
        else:
            return False

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print(data.decode())
        self.buffer += data
        if not self.has_full_packet(self.buffer): #check if buffer have "\r\n\r\n"
            return
        else:
            buffer_string = self.buffer.decode()

            first_string = buffer_string.split("\r\n")[0]
            first_list = first_string.split(" ")

            error_string = "HTTP/1.1 404 Not Found" +"Date: "+str(datetime.datetime.now())+"\r\n" + "Content-Length: 0\r\n" + "Server: NetSec Prototype Server 1.0\r\n\r\n"
            if first_list[0] == "GET":
                if first_list[2] == "HTTP/1.1" or first_list[2] == "HTTP/1.0":
                    uri_string = self.document_root + first_list[1]
                    my_file = Path(uri_string)

                    if my_file.is_file():
                        fsize = os.path.getsize(uri_string)
                        file = open(uri_string, mode='rb')
                        data = file.read()
                        str1 = "HTTP/1.1 200 OK\r\n Date: "+str(datetime.datetime.now())+"\r\n Server: NetSec Prototype Server 1.0\r\n Last-Modified: "+str(datetime.datetime.now())+"\r\n"
                        response = str1 + "Content-Length: "+ str(fsize) +"\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n"
                        self.transport.write(response.encode())
                        self.transport.write(data)
                    else:
                        self.transport.write(error_string.encode())
                else:
                    self.transport.write(error_string.encode())
            else:
                self.transport.write(error_string.encode())


# /Users/wang/PycharmProjects/netsec/www_server
document_root =  sys.argv[1] # first command line parameter
loop = asyncio.get_event_loop()
coro = loop.create_server(lambda: ExampleHttpServer(document_root), '127.0.0.1', 8280)
server = loop.run_until_complete(coro)
# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.run_until_complete(server.wait_closed())
