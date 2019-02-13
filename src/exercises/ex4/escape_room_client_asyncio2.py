import asyncio
from aioconsole import ainput
import sys

stdin_queue = []

class EscapeClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.sign = 0

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.sign = 1
        if "escaped" not in data.decode() and "dead" not in data.decode():
            print(data.decode())
        else:
            print(data.decode())
            self.transport.close()

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

def handle_stdin():
    line_in = sys.stdin.readline()
    line_in = line_in[:-1] # remove \n
    stdin_queue.append(line_in)

async def async_input(prompt):
    print(prompt, end="")
    sys.stdout.flush()
    while len(stdin_queue) == 0:
        await asyncio.sleep(.1)
    return stdin_queue.pop(0)

async def game_runner(protocol):
    while True:
        command = await async_input(">> ")
        protocol.transport.write(command.encode())

        while protocol.sign == 0:
            await asyncio.sleep(0.001)
        protocol.sign = 0
        # await a response... see if you can figure this part out!

loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda:EscapeClientProtocol(loop),'', 7888)

transport, protocol = loop.run_until_complete(coro)

loop.add_reader(sys.stdin, handle_stdin) # setup the call-back!
asyncio.ensure_future(game_runner(protocol))
loop.run_forever()
loop.close()
