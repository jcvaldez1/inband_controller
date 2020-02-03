from flask import Flask, request
import requests
from threading import Thread
import socket
import queue
import time
application = Flask(__name__)
commands = {}
threads = []

class hyper(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("0.0.0.0", 42915))
        self.s.listen()
    def run(self):
        while True:
            c, addr = self.s.accept()
            #threading.start_new_thread(on_new_client,(c,addr))
            Thread(target=on_new_client,args=(c,addr))


def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        #do some checks and if msg == someWeirdSignal: break:
        #print addr, ' >> ', msg
        print(msg)
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.send(msg)
    clientsocket.close()


"""
class listener(Thread):
    def __init__(self,deviceID):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("0.0.0.0", 42915))
        self.deviceID = deviceID
        self.msgQueue = queue.Queue()

    def run(self):
        print("port " + str(self.s.getsockname()[1]) + " opened")
        self.s.listen()
        print("good")
        conn, addr = self.s.accept()
        print('Connected at' + str(self.s.getsockname()[1]))
        while True:
            if not self.msgQueue.empty():
                item = self.msgQueue.get()
                conn.sendall(item)
            time.sleep(0.5)
    def get_port(self):
        return str(self.s.getsockname()[1])
"""

def process_request(req):
    print(req)
    for val in list(commands.values()):
        if val['signal'] == req['signal'] or val['signal'] == 'any':
            if val['deviceID'] == req['deviceID']:
                if val['commType'] == "forward":
                    r = requests.post(url=val['targetIP'],json=req  )
                    return r.text
                elif val['commType'] == "device":
                    for thread in threads:
                        if thread.deviceID == req['deviceID']:
                            thread.msgQueue.put(str(val['sayThis']).encode('utf-8'))
                    return "sent to device"
    return "nothing found"
    
            

@application.route("/config", methods=["POST"])
def config():
    buffer = request.get_json()
    commands[buffer["commandID"]] = buffer["commandDetails"]
    print(commands)
    return "cool", 200

@application.route("/report", methods=["POST"])
def report():
    buffer = request.get_json()
    process_request(buffer)
    return "cool", 200

"""
@application.route("/open_channel", methods=["POST"])
def open_channel():
    buffer = request.get_json()
    deviceID = buffer["deviceID"]
    x = listener(deviceID)
    threads.append(x)
    threads[-1].start()
    #return port number
    return x.get_port(), 200
"""

if __name__ == "__main__":
    bigboy = hyper()
    bigboy.start()
    application.run(port=80, host="0.0.0.0", debug=False)