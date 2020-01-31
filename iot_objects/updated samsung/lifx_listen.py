import websocket
import re
import sys
from time import sleep
import datetime
import socket
import json
import requests

from lifxlan import LifxLAN, RED, GREEN, BLUE, CYAN, YELLOW, PINK

def toggle_device_power(device, state):
    if state == "on":
        device.set_power("on", True)
    else:
        device.set_power("off", True)

def on_message(ws, message):
    message = message.decode("utf-8")
    print(message)
    #print(datetime.datetime.now())
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
def on_error(ws, error):
    print(error)
    
def on_close(ws):
    #ws.close()
    print("closed")

def on_open(ws):
    ws.send("RPI")        
    print("open")

def enroll():
    temp = requests.post(url = 'http://13.55.147.2/enroll', data = "hello", timeout = 5)
    print(temp.text)

def send_dummy():
    print("in")
    UDP_IP_ADDRESS = "69.4.20.69"
    UDP_PORT_NO = 420

    data = {
        'ports':[6,9],
        'name': 'samsung',
        'cloud_ip': '69.4.20.69'
    }

    data_json = json.dumps(data)

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto(bytes(data_json,'utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
        
if __name__ == "__main__":
    ##SNIFF BULBS FIRST##
    lifx = LifxLAN()
    devices = lifx.get_lights()
    bulb = devices[0]
    
    toggle_device_power(bulb, "on")
    lifx.set_color_all_lights(BLUE, rapid = True)

    #enroll()
    #send_dummy()
    
    while True:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://13.55.147.2:42915/", on_message = on_message, on_error = on_error, on_close = on_close)
        ws.on_open = on_open
        ws.run_forever(ping_interval = 30, ping_timeout = 10)

