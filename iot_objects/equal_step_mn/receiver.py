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
import makedir

receiver_log_file = None


def on_message(ws, message):
    message = message.decode("utf-8")
    print(message)
    msg_log = makedir.safe_open_w(receiver_log_file)
    msg_log.write(str(datetime.datetime.now()) + " " + message + "\n")
    msg_log.close()

def on_error(ws, error):
    print(error)
    
def on_close(ws):
    ws.close()
    print("closed")

def on_open(ws):
    ws.send(str(host_name))        
    print("open")

        
if __name__ == "__main__":
    ##SNIFF BULBS FIRST##
    if len(sys.argv) < 3:
        print("Usage: python3 receiver.py <host_number> <receiver_cloud_ip>")
        sys.exit(1)
    host_name = sys.argv[1]
    lifx_ip = sys.argv[2]
    receiver_log_file = "./results/receiver/"+str(lifx_ip)+"/"+str(host_name)+"_receiver.log"

    
    while True:
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("ws://"+str(lifx_ip)+":42915" , on_message = on_message, on_error = on_error, on_close = on_close)
        ws.on_open = on_open
        ws.run_forever(ping_interval = 30, ping_timeout = 10)

