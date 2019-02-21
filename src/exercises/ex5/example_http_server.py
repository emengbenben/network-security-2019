import asyncio
import sys
import datetime
import os.path
import time
import mimetypes
from pathlib import Path
import glob
import stat

def getMdate(file):
    '''return: modified time of a file'''
    # os.stat return properties of a file
    tmpTime = time.localtime(os.stat(file).st_mtime)
    return time.strftime('%Y-%m-%d', tmpTime)

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

    def connection_lost(self, exc):
        # The socket has been closed, stop the event loop
        loop.stop()
    def data_received(self, data):
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
                        #get the size of the file
                        fsize = os.path.getsize(uri_string)
                        file = open(uri_string, mode='rb')
                        data = file.read()

                        modify_time = getMdate(uri_string)

                        # Use Python's MimeTypes module to return the correct type for different types of files based on extension
                        name_list = first_list[1].split("/")
                        file_name = mimetypes.guess_type(name_list[-1])

                        str1 = "HTTP/1.1 200 OK\r\nDate: "+str(datetime.datetime.now())+"\r\nServer: NetSec Prototype Server 1.0\r\nLast-Modified: "+str(modify_time)+"\r\n"
                        response = str1 + "Content-Length: "+ str(fsize) +"\r\nConnection: close\r\nContent-Type: "+ file_name[0]+"\r\n\r\n"
                        print(response)
                        self.transport.write(response.encode())
                        self.transport.write(data)
                    elif my_file.is_dir(): #if uri is a directory
                        uri_string += "index.html"
                        my_newfile = Path(uri_string)

                        if my_newfile.is_file():  # if index.html is present
                            fsize = os.path.getsize(uri_string)
                            file = open(uri_string, mode='rb')
                            data = file.read()
                            # identify the type of the file- idnex.html
                            file_name = mimetypes.guess_type("index.html")

                            modify_time = getMdate(uri_string)

                            str1 = "HTTP/1.1 200 OK\r\n Date: " + str(datetime.datetime.now()) + "\r\n Server: NetSec Prototype Server 1.0\r\n Last-Modified: " + str(modify_time) + "\r\n"
                            response = str1 + "Content-Length: " + str(fsize) + "\r\nConnection: close\r\nContent-Type: " + file_name[0] + "\r\n\r\n"
                            self.transport.write(response.encode())
                            self.transport.write(data)
                        else:
                            self.transport.write(error_string.encode())
                    else:
                        self.transport.write(error_string.encode())
                else:
                    self.transport.write(error_string.encode())
            else:
                self.transport.write(error_string.encode())
            self.buffer = bytes()

# example_http_server.py "/Users/wang/PycharmProjects/netsec/www_server"
document_root = sys.argv[1] # first command line parameter
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
