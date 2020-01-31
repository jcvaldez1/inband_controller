"""

    Receiver IoT device emulator, will simply open a websocket
    connection to the registered cloud and log reception time

"""
import websocket
import re
import sys
from time import sleep
import datetime
import socket
import json
import requests
from constants import *

def on_message(ws, message):
    message = message.decode("utf-8")
    print(message)
    msg_log = open(RECEIVER_LOG_FILE, "a+")
    msg_log.write(str(datetime.datetime.now()) + " " + message + "\n")
    msg_log.close()

def on_error(ws, error):
    print(error)
    
def on_close(ws):
    ws.close()
    print("closed")

def on_open(ws):
    ws.send("RPI")        
    print("open")

        
if __name__ == "__main__":
    ##SNIFF BULBS FIRST##
    
    while True:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(LIFX_CLOUD , on_message = on_message, on_error = on_error, on_close = on_close)
        ws.on_open = on_open
        ws.run_forever(ping_interval = 30, ping_timeout = 10)

