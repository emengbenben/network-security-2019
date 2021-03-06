import asyncio
from aioconsole import ainput
import sys
class EscapeClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        self.transport = transport

    def data_received(self, data):
        if "escaped" not in data.decode() and "dead" not in data.decode():
            print(data.decode())
            command = stdinAlert()
            self.transport.write(command.encode())
        else:
            print(data.decode())
            self.transport.close()

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

def stdinAlert():
    lines = sys.stdin.readline()
    return lines

loop = asyncio.get_event_loop()

loop.add_reader(sys.stdin, stdinAlert)

message = stdinAlert()

coro = loop.create_connection(lambda: EscapeClientProtocol(message, loop),
                              '127.0.0.1', 7888)
loop.run_until_complete(coro)
loop.run_forever()
