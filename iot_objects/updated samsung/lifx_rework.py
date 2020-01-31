import websockets
import asyncio
import requests
import datetime

from lifxlan import LifxLAN, RED, GREEN, BLUE, CYAN, YELLOW, PINK

def toggle_device_power(device, state):
    if state == "on":
        device.set_power("on", True)
    else:
        device.set_power("off", True)

def resolve(message,bulb,lifx):
    message = message.decode("utf-8")
    print(message)
    msg_log = open("bulb_log.txt", "a")
    msg_log.write(str(datetime.datetime.now()) + " " + message + "\n")
    msg_log.close()

    if "on" in message:
        toggle_device_power(bulb, "on")
    elif "off" in message:
        toggle_device_power(bulb, "off")
    elif "red" in message:
        lifx.set_color_all_lights(RED, rapid = True)
    elif "blue" in message:
        lifx.set_color_all_lights(BLUE, rapid = True)
    elif "green" in message:
        lifx.set_color_all_lights(GREEN, rapid = True)
    elif "cyan" in message:
        lifx.set_color_all_lights(CYAN, rapid = True)
    elif "yellow" in message:
        lifx.set_color_all_lights(YELLOW, rapid = True)
    elif "pink" in message:
        lifx.set_color_all_lights(PINK, rapid = True)

async def hello():
    #lifx = LifxLAN()
    #devices = lifx.get_lights()
    #bulb = devices[0]
    #toggle_device_power(bulb, "on")
    uri = "ws://13.55.147.2:42915"
    print(uri)
    async with websockets.connect(uri) as websocket:
        await websocket.send("RPI") #set device ID
        while True: #main logic loop
            incoming = await websocket.recv()
            #resolve(incoming,bulb,lifx)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())