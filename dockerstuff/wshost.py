#!/usr/bin/env python

# WS server example

import asyncio
import websockets
from threading import Thread
from time import sleep

async def hello(websocket, path):
    print("OWO")
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

class hyper(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(hello, "0.0.0.0", 42915)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


foo = hyper()
foo.start()

while True:
    print("hewwo")
    sleep(30)

#print('Received', repr(data))