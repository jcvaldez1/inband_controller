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

receiver_log_file = None
host_name = None

def on_message(ws, message):
    message = message.decode("utf-8")
    print(message)
    msg_log = open(receiver_log_file, "a+")
    msg_log.write(str(datetime.datetime.now()) + " " + message + "\n")
    msg_log.close()

def on_error(ws, error):
    print(error)
    
def on_close(ws):
    ws.close()
    print("closed")

def on_open(ws):
    ws.send(str(host_number))        
    print("open")

        
if __name__ == "__main__":
    ##SNIFF BULBS FIRST##
    if len(sys.argv) < 2:
        print("Usage: python3 receiver.py <host_number>")
        sys.exit(1)
    host_name = sys.argv[1]
    receiver_log_file = "./results/receiver/"+str(host_name)+"_receiver_log.log"

    
    while True:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(LIFX_CLOUD , on_message = on_message, on_error = on_error, on_close = on_close)
        ws.on_open = on_open
        ws.run_forever(ping_interval = 30, ping_timeout = 10)

