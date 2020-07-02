from flask import Flask, request, render_template, jsonify
import requests
from threading import Thread, Lock
import socket
import queue
import time
import asyncio
import select
import websockets
import dummy_config

application = Flask(__name__)
global commands
commands = dummy_config.SG_CONF
commands.update(dummy_config.AUS_CONF)
threads = []
goods = []
msgQueue = queue.Queue()
grouping =  {}


async def hello(websocket, path):
    print("thread hello")
    name = await websocket.recv()
    print(name)
    ctr = 0
    while True:
        if ctr == 30:
            try:
                await websocket.ping()
            except:
                await websocket.close()
            ctr = 0 
        if not msgQueue.empty():
            print('msgQ has stuff')
            to_send = msgQueue.get()
            if to_send[1] == name:
                await websocket.send(to_send[0])
            else:
                msgQueue.put(to_send)
        ctr += 1
        await asyncio.sleep(0.05)

class hyper(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        print("go thread")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(ws_handler=hello, host="0.0.0.0", port=42915)
        
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
bigboy = hyper()
#msgQueue = queue.Queue()

def process_request(req):
    global doge
    print(req)
    for val in list(commands.values()):
        if val['signal'] == req['signal'] or val['signal'] == 'any':
            if val['deviceID'] == req['deviceID']:
                if val['commType'] == "forward":
                    doge = val['targetIP']
                    r = requests.post(url=val['targetIP'],json=req)
                    return r.text
                elif val['commType'] == "device":
                    if "sequence_num" in req:
                        msgQueue.put((str(val['sayThis']+" "+str(req['sequence_num'])).encode('utf-8'),val['target']))
                    else:
                        msgQueue.put((str(val['sayThis']).encode('utf-8'),val['target']))
                    return "sent to device"
    return "nothing found"

@application.route("/enroll", methods=["POST"])
def enroll():
    buffer = request.get_json()
    #return "device enrolled", 200
    #check if it exists first
    if buffer['group'] not in grouping:
        grouping[buffer['group']] = []
    grouping[buffer['group']].append(buffer['deviceID'])
    print(grouping)
    return "cool", 200
@application.route("/reset", methods=["POST"])
def reset():
    global commands
    commands = {}
    return "cool", 200

@application.route("/config", methods=["POST"])
def config():
    buffer = request.get_json()
    commands[buffer["commandID"]] = buffer["commandDetails"]
    print(commands)
    return "cool", 200

@application.route("/config_multi", methods=["POST"])
def config_multi():
    buffer = request.get_json()
    for k in buffer:
        commands[k["commandID"]] = k["commandDetails"]
    print(commands)
    return "cool", 200


@application.route("/report", methods=["POST"])
def report():
    #print(msgQueue)
    #print(goods)
    buffer = request.get_json()
    process_request(buffer)
    return "cool", 200

@application.route('/')
def index():
    return render_template('home.html')

@application.route('/contact_cloud')
def contact_cloud():
    buffer = request.get_json()
    r = requests.get(url=(buffer['cloud']+'/return_config'))
    return r

@application.route("/return_group", methods=["GET"])
def gib_groop():
    if 'group' in request.args:
        return jsonify(grouping[request.args['group']])
    return jsonify(commands)

@application.route("/return_group_config", methods=["GET"])
def gib_groop_conf():
    if 'group' in request.args:
        config_out = []
        for k,v in commands.items():
            if v['group'] == request.args['group']:
                config = {'commandID':k,'commandDetails':v}
                config_out.append(config)
        return jsonify(config_out)
    return jsonify(commands)

@application.route("/return_group_config_multi", methods=["GET"])
def gib_groop_conf_multi():
    if 'group' in request.json:
        config_out = {}
        for group in request.json['group']:
            buffer = []
            for k,v in commands.items():
                if v['group'] == group:
                    config = {'commandID':k,'commandDetails':v}
                    buffer.append(config)
            config_out[group] = buffer
        return jsonify(config_out)
    return jsonify(commands)

@application.route("/return_config", methods=["GET"])
def gib_config():
    config_out = []
    if 'deviceID' in request.args:
        for k,v in commands.items():
            if v['deviceID'] == request.args['deviceID']:
                config = {'commandID':k,'commandDetails':v}
                config_out.append(config)
        return jsonify(config_out)
    return jsonify(commands)

bigboy.start()
#smolboy.start()
if __name__ == '__main__':
    application.run(port=80, host="0.0.0.0", debug=False)
