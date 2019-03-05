import asyncio
from escape_room import EscapeRoom
import playground

class EscapeServerClientProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))

        self.transport = transport

        self.room = EscapeRoom()
        self.room.start()
    def data_received(self, data):
        string = data.decode()
        string = string[:-1]
        output = self.room.command(string)
        self.transport.write(output.encode())

        status = self.room.status()
        if status == "dead":
            self.transport.write(("\r\n"+status).encode())
        elif status == "escaped":
            if string == "open door":
                self.transport.write(("\r\n"+status).encode())

loop = asyncio.get_event_loop()

# Each client connection will create a new protocol instance
coro = playground.create_server(EscapeServerClientProtocol, '20191.10.20.30', 62261)

server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}')
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.run_until_complete(server.wait_closed())
