import asyncio
from escape_room import EscapeRoom

class EscapeServerClientProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))

        self.transport = transport

        self.room = EscapeRoom()
        self.room.start()
    def data_received(self, data):
        output = self.room.command(data.decode())
        self.transport.write(output.encode())

        status = self.room.status()
        if status == "dead":
            self.transport.write(("\r\n"+status).encode())
        elif status == "escaped":
            if data.decode() == "open door":
                self.transport.write(("\r\n"+status).encode())


        #print('Close the client socket')
        #self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EscapeServerClientProtocol, '127.0.0.1', 7888)

server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

loop.run_until_complete(server.wait_closed())